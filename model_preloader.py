import os
import torch
from annotator.offline.train_utils import load_model

project_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(project_dir, './annotator/offline/logs/complete/models')
model_file = 'model_epoch-3_dev-macro-f1-0.4716132465835384_dev-loss-16.142220458984376_2019-04-23__08-51__925007.pt'

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model, text_encoder, label_encoder = load_model(save_dir, model_file=model_file)
model = model.to(device)
n_ctx = model.n_ctx
max_len = 512 // 3
