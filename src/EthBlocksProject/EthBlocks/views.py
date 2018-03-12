# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

logger = logging.getLogger(__name__)
from django.shortcuts import render, redirect
from django.http import JsonResponse


from . import services

# Create your views here.

def index(request):
    return render(request, 'EthBlocks/index.html')

def latestBlockInfo(request):
    logger.debug("in latesBlockInfo")
    blockhash = services.getLatestBlockHash()
    logger.debug("blockhash")
    logger.debug(blockhash)
    return redirect('/' + blockhash)

def blockInfo(request, hash):
    logger.debug("hash length")
    logger.debug(hash)
    logger.debug(len(hash))
    if len(hash) != 64:
        return render(request, 'EthBlocks/not-found.html')
    else:
        logger.debug("in blockInfo.. ")
        logger.debug(hash)
        #if hash is None:
        #Find latest block hash and redirect to page with hash id.
        block = services.getBlock(hash)
        if block:
            block_to_save_dict = {
                'height': block.height,
                'hash': block.hash,
                'n_tx': block.n_tx,
                'received_time': block.received_time,
                'prev_block': block.prev_block,
                'next_block': block.next_block
            }
            logger.debug("rednering...")
            return render(request, 'EthBlocks/eth-blocks.html', block_to_save_dict)
        else:
            return render(request, 'EthBlocks/not-found.html')

# def blockInfoJSON(request, hash):
#     logger.debug("in blockInfoJSON")
#     logger.debug(hash)
#     block = services.getBlock(hash)
#
#     block_to_save_dict = {
#         'height': block.height,
#         'hash': block.hash,
#         'n_tx': block.n_tx,
#         'received_time': block.received_time,
#         'prev_block': block.prev_block,
#         'next_block': block.next_block
#     }
#     return JsonResponse(block_to_save_dict)
#



