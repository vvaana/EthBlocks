import datetime
import logging

import requests
from django.utils.timezone import utc
from django.core.exceptions import ObjectDoesNotExist

from .models import BlockInfo

logger = logging.getLogger('console')

TIME_TO_CACHE_LATEST_BLOCK = 3600

def getBlockBCAndSaveItToDB(hash):
    logger.debug("In getBlockBCAndSaveItToDB")
    response = requests.get('https://api.blockcypher.com/v1/dash/main/blocks/' + hash)
    logger.debug("response")
    logger.debug(response)
    try:
        block = response.json()
    except JSONDecodeError:
        return None

    logger.debug("block")
    logger.debug(block)
    if 'height' in block:
        format = "%Y-%m-%dT%H:%M:%SZ"
        datetime_obj = datetime.datetime.strptime(block['received_time'], format)
        logger.debug("blockModel")
        blockModel = BlockInfo(
            height = block['height'],
            hash = block['hash'],
            n_tx = block['n_tx'],
            received_time = datetime_obj,
            prev_block = block['prev_block']
        )
        logger.debug(blockModel)
        blockModel.save()
        findPreviousBlockAndUpdateNextHash(blockModel)
        findBlockByPreviousAndUpdateNextHash(blockModel)

        return blockModel
    else:
        return None

def getLatestBlockHashBC():
    logger.debug("In getLatestBlockHashBC")
    response = requests.get('https://api.blockcypher.com/v1/dash/main')
    block = response.json()
    logger.error("block for hash")
    logger.debug(block)

    return block['hash']

#Get latest block hash from database.
#If latest block is older than an hour, get hash  of the last block from service.
def getLatestBlockHash():
    logger.debug("In getLatestBlockHashDb")
    try:
        blockModel = BlockInfo.objects.all().order_by("-height").first()
        logger.debug("blockModel")
        logger.debug(blockModel)
        if blockModel:
            blockHash = blockModel.hash;

            # Calculate time that passed.
            if deltaTime(blockModel.modified_date) > TIME_TO_CACHE_LATEST_BLOCK:
                logger.debug("Fetching latest block from service.")
                blockHash = getLatestBlockHashBC()
        else:
            blockHash = getLatestBlockHashBC()
    except ObjectDoesNotExist:
        blockHash = getLatestBlockHashBC()

    return blockHash

def getLatestBlock():
    #Find latest block in cache (block with max height)
    blockModel = BlockInfo.objects.all().order_by("-height").first()
    if blockModel:
        #Calculate time that passed.
        #If more than an hour passed, call an actual service and get latest block.
        if deltaTime(blockModel.modified_date) > TIME_TO_CACHE_LATEST_BLOCK:
            logger.debug("Fetching latest block from service.")
            blockHash = getLatestBlockHash()
            blockModel = getBlock(blockHash)
    return blockModel

def getBlock(hash):
    try:
        logger.debug("Block from database")
        blockModel = BlockInfo.objects.get(hash=hash)
    except ObjectDoesNotExist:
        logger.debug(("Call api"))
        blockModel = getBlockBCAndSaveItToDB(hash)
    return blockModel

def deltaTime(modifiedDate):
    if modifiedDate:
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff = now - modifiedDate
        return timediff.total_seconds()

def findPreviousBlockAndUpdateNextHash(currentBlock):
    try:
        prevBlock = BlockInfo.objects.get(hash=currentBlock.prev_block)
        prevBlock.nextHash = currentBlock.hash
        prevBlock.save()
        return prevBlock.hash
    except ObjectDoesNotExist:
        return None

#Find next block.
#Update current blocks' next_block.
def findBlockByPreviousAndUpdateNextHash(currentBlock):
    try:
        nextBlock = BlockInfo.objects.get(prev_block=currentBlock.hash)
        currentBlock.next_block = nextBlock.hash
        currentBlock.save()
        return nextBlock.hash
    except ObjectDoesNotExist:
        return None

