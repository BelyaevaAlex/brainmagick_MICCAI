# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""Models to be applied on the features before applying the contrastive loss.
"""

from .common import ConvSequence
import logging
from torch import nn
import torch
import typing as tp

logger = logging.getLogger(__name__)


class DeepMel(ConvSequence):
    """DeepMel model that extracts features from the Mel spectrogram.

    Parameters
    ----------
    n_in_channels :
        Number of input channels.
    n_hidden_channels :
        Number of channels in hidden layers.
    n_hidden_layers :
        Number of hidden layers.
    n_out_channels :
        Number of output channels.
    kwargs:
        Additional keyword arguments to pass to ConvSequence.
    """
    def __init__(self, n_in_channels: int, n_hidden_channels: int, n_hidden_layers: int,
                 n_out_channels: int, **kwargs):
        channels = \
            [n_in_channels] + [n_hidden_channels] * (n_hidden_layers - 1) + [n_out_channels]
        super().__init__(channels, **kwargs)


class ConvWave(nn.Module):
    def __init__(self, input_channels: int =1024,
                 kernel_sizes: tp.Sequence[int] =[3,3], 
                 strides: tp.Sequence[int] =[1,1],
                 adaptive_pool : bool = False, 
                 adaptive_pooling_size: int  = 1,
                 dropout_value: float = 0.2,
                 n_out_channels: int = 512):
        super().__init__()
        print("ConvWave")
        self.n_out_channels = n_out_channels
        self.first_layer = nn.Conv1d(in_channels=input_channels, out_channels = n_out_channels, kernel_size=kernel_sizes[0], stride=strides[0], padding =1)
        self.dropout = nn.Dropout(p=dropout_value)
        self.adaptive_pool = None
        if adaptive_pool:
            self.adaptive_pool =  nn.AdaptiveAvgPool1d(output_size=adaptive_pooling_size)
        
    def forward(self, x):
        x = self.first_layer(x)
        if self.adaptive_pool  is not None:
            x = self.adaptive_pool(x)
        x = self.dropout(x)    
        return x