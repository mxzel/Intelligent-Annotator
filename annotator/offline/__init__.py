from os import path

import os, sys
import torch

from tempfile import NamedTemporaryFile

from sklearn.metrics import accuracy_score, precision_recall_fscore_support

from annotator.offline.model_pytorch import DoubleHeadModel, load_openai_pretrained_model, dotdict

from annotator.offline.datasets import SemEval2010Task8

from annotator.offline.train_utils import predict, iter_data, iter_apply, persist_model, load_model
from annotator.offline.logging_utils import ResultLogger
from annotator.offline.analysis_util import evaluate_semeval2010_task8
from . import text_utils

sys.modules['text_utils'] = text_utils
# print(sys.modules)

"""
evaluate(
        dataset='semeval_2010_task8',
        masking_mode='unk',
        test_file='./annotator/offline/datasets/SemEval2010_task8/test.jsonl',
        save_dir='./annotator/offline/logs/complete/models',
        model_file='model_epoch-3_dev-macro-f1-0.4716132465835384_dev-loss-16.142220458984376_2019-04-23__08-51__925007.pt',
        batch_size=8,
        log_dir='./annotator/offline/logs/'
    )
"""


def evaluate(dataset, test_file, log_dir, save_dir, model_file='model.pt', batch_size=8, masking_mode=None):
    # with open('test123123.txt', mode='w') as fw:
    #     fw.write('\n')

    cfg = dotdict(locals().items())
    print(cfg)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model, text_encoder, label_encoder = load_model(save_dir, model_file=model_file)

    model = model.to(device)

    n_special = 4

    n_ctx = model.n_ctx
    max_len = 512 // 3

    test = SemEval2010Task8._load_from_jsonl(test_file, is_test=False, masking_mode=masking_mode)
    test = SemEval2010Task8.encode(test, text_encoder=text_encoder, label_encoder=label_encoder)
    test = SemEval2010Task8.transform(*test, text_encoder=text_encoder, max_length=max_len, n_ctx=n_ctx)[0]

    negative_label = 'Other'

    indices_test, _, label_idxs_test, ids_test, entity_ids_test = test

    log_pr_curve = entity_ids_test is not None

    # import pudb
    # pudb.set_trace()

    label_idxs_pred, probs_test = predict(indices_test, model, device, batch_size, compute_probs=log_pr_curve)
    labels_pred_test = [label_encoder.get_item_for_index(label_index) for label_index in label_idxs_pred]






def predict_data(test_file, save_dir, model_file='model.pt', batch_size=8, masking_mode=None):
    cfg = dotdict(locals().items())

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model, text_encoder, label_encoder = load_model(save_dir, model_file=model_file)
    model = model.to(device)

    n_special = 4
    n_ctx = model.n_ctx
    max_len = 512 // 3

    test = SemEval2010Task8._load_from_jsonl(test_file, is_test=True, masking_mode=masking_mode)
    test = SemEval2010Task8.encode(
        test, text_encoder=text_encoder, label_encoder=label_encoder)
    test = SemEval2010Task8.transform(
        *test, text_encoder=text_encoder, max_length=max_len, n_ctx=n_ctx)[0]

    negative_label = 'Other'

    indices_test, _, _, _, _ = test

    label_idxs_pred, probs_test = predict(
        indices_test, model, device, batch_size, compute_probs=False)
    labels_pred_test = [label_encoder.get_item_for_index(label_index)
                        for label_index in label_idxs_pred]

    return labels_pred_test


if __name__ == '__main__':
    evaluate(
        dataset='semeval_2010_task8',
        masking_mode='unk',
        test_file='./annotator/offline/datasets/SemEval2010_task8/test.jsonl',
        save_dir='./annotator/offline/logs/complete/models',
        model_file='model_epoch-3_dev-macro-f1-0.4716132465835384_dev-loss-16.142220458984376_2019-04-23__08-51__925007.pt',
        batch_size=8,
        log_dir='./annotator/offline/logs/'
    )
