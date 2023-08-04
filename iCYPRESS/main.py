import logging
import os

import torch
from torch_geometric import seed_everything
from deepsnap.dataset import GraphDataset
from graphgym.cmd_args import parse_args
from graphgym.config import cfg, dump_cfg, load_cfg, set_run_dir, set_out_dir
from graphgym.loader import create_dataset, create_loader
from graphgym.logger import create_logger, setup_printing
from graphgym.model_builder import create_model
from graphgym.optimizer import create_optimizer, create_scheduler
from graphgym.register import train_dict
from graphgym.train import train
from graphgym.utils.agg_runs import agg_runs
from graphgym.utils.comp_budget import params_count
from graphgym.utils.device import auto_select_device
from graphgym.models.gnn import GNNStackStage
from CytokinesDataSet import CytokinesDataSet
from Visualization import Visualize
from graphgym.models.layer import GeneralMultiLayer, Linear, GeneralConv
from graphgym.models.gnn import GNNStackStage

if __name__ == '__main__':
    # Load cmd line args
    args = parse_args()
    # Load config file
    load_cfg(cfg, args)
    set_out_dir(cfg.out_dir, args.cfg_file)
    # Set Pytorch environment
    torch.set_num_threads(cfg.num_threads)
    dump_cfg(cfg)
    # Repeat for different random seeds
    for i in range(args.repeat):
        set_run_dir(cfg.out_dir)
        setup_printing()
        # Set configurations for each run
        cfg.seed = cfg.seed + 1
        seed_everything(cfg.seed)
        auto_select_device()
        # Set machine learning pipeline
        datasets = create_dataset()


        # last 6 are testing

        dataset_all = []
        dataset_all += datasets[0]
        dataset_all += datasets[1]
        merged_dataset = GraphDataset(dataset_all, minimum_node_per_graph = 0)
        offset = int(len(merged_dataset) / 2)


        correct = 0
        total = 0
        for i in range(offset):
            new_test_dataset = []
            new_train_dataset = []

            for j in range(len(dataset_all)):
                if j == i or j == i + offset:
                    new_test_dataset.append(dataset_all[j])
                else:
                    new_train_dataset.append(dataset_all[j])
            
            new_test_dataset = GraphDataset(new_test_dataset, minimum_node_per_graph = 0)
            new_train_dataset = GraphDataset(new_train_dataset, minimum_node_per_graph = 0)
            datasets[0] = new_train_dataset
            datasets[1] = new_test_dataset



            loaders = create_loader(datasets)
            loggers = create_logger()
            model = create_model()





            # Add edge_weights attribute to the datasets so that they can be accessed in batches
            num_edges = len(datasets[0][0].edge_index[0])
            edge_weights = torch.nn.Parameter(torch.ones(num_edges))
            for loader in loaders:
                for dataset in loader.dataset:
                    dataset.edge_weights = edge_weights


            #add edge weights to the set of parameters
            newParam = list()
            for param in model.parameters():
                newParam.append(param)
            
            newParam.append(edge_weights)

            optimizer = create_optimizer(newParam)
            scheduler = create_scheduler(optimizer)
            # Print model info
            logging.info(model)
            logging.info(cfg)
            cfg.params = params_count(model)
            logging.info('Num parameters: %s', cfg.params)
            # Start training
            if cfg.train.mode == 'standard':
                train(loggers, loaders, model, optimizer, scheduler)
            else:
                train_dict[cfg.train.mode](loggers, loaders, model, optimizer,
                                        scheduler)
                

            for batch in loaders[1]:
                print("here")
                pred, true = model(batch)
                # this only works in this very specific case. Work needs to be done to generalize it
                if(pred[0] < 0.5):
                    correct += 1

                if(pred[1] > 0.5):
                   correct +=1
                
                total += 2


        

            
        print("correct")
        print(correct)
        print("total")
        print(total)
                
    """
    # Aggregate results from different seeds
    agg_runs(cfg.out_dir, cfg.metric_best)
    # When being launched in batch mode, mark a yaml as done
    if args.mark_done:
        os.rename(args.cfg_file, f'{args.cfg_file}_done')

    

    name = cfg.dataset.name.split(",")[1]

    last_layers_pooled = []
    truths = []

    for loader in loaders:
        for batch in loader:
            last_layer_pooled, truth = model.get_last_hidden_layer_pooled(batch) # first one gives me the vector output of the neural network. 
            last_layers_pooled += last_layer_pooled
            truths.append(truth)

    last_layer_tensor = torch.stack(last_layers_pooled)
    truths_tensor = torch.cat(truths)

    numpy_matrix = last_layer_tensor.numpy()
    numpy_truth = truths_tensor.numpy()

    correlations = []

    for loader in loaders:
        for batch in loader:
            correlation = model.get_correlations(batch) # first one gives me the vector output of the neural network. 
            correlations += correlation


    Visualize.visualize_correlations(name, datasets[0].graphs[0].G, correlations[0])

    Visualize.visualize_TSNE(numpy_matrix, numpy_truth)


    for child in model.children(): # We are at the network level.
        if(isinstance(child, GeneralMultiLayer)): 
            for grandchild in child.children(): # we are at the MultiLayer object
                for object in grandchild.children(): # we are at the GeneralLayer object
                    if(isinstance(object, Linear)):
                        for layer in object.children(): # we are at the Linear object
                            colorWeights = layer.weight

    Visualize.visualize_graph(colorWeights, datasets[0].graphs[0].G, name, edge_weights)
    




"""