#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
get.py
"""

import logging
import requests
import json

logger = logging.getLogger(__name__)


def tweets(url):
    """

    """
    twitter_count = "http://urls.api.twitter.com/1/urls/count.json?url=%s"
    query = twitter_count % (url)
    resp = requests.get(query)

    if resp.status_code == 200:
        return (
            json.loads(resp.text)['count'],
        )
    else:
        raise Exception


def linkedin(url):
    linkedin_count = \
        "http://www.linkedin.com/countserv/count/share?url=%s&format=json"
    query = linkedin_count % (url)
    resp = requests.get(query)

    if resp.status_code == 200:
        return (
            json.loads(resp.text)['count'],
        )
    else:
        raise Exception


def facebook(url):
    facebook_count = \
        'http://graph.facebook.com/%s'
    query = facebook_count % (url)
    resp = requests.get(query)

    if resp.status_code == 200:
        js = json.loads(resp.text)
        return (
            js.get('shares', 0),
            js.get('likes', 0),
            js.get('comments', 0),
        )
    else:
        raise Exception


def plusone(url):
    queryurl = "https://clients6.google.com/rpc"
    params = {
        "method": "pos.plusones.get",
        "id": "p",
        "params": {
            "nolog": True,
            "id": "%s" % (url),
            "source": "widget",
            "userId": "@viewer",
            "groupId": "@self",
        },
        "jsonrpc": "2.0",
        "key": "p",
        "apiVersion": "v1"
    }
    headers = {
        'Content-type': 'application/json',
    }

    try:
        resp, content = requests.post(
            queryurl,
            data=json.dumps(params),
            headers=headers
            )
        if resp.status_code == 200:
            result_json = json.loads(resp.text)
            result = int(
                result_json['result']['metadata']['globalCounts']['count']
            )
    except ValueError as e:
        logger.error(e)
        logger.error(json.dumps(params))
        logger.error(headers)
    except Exception as e:
        logger.error("""stop: counting +1s. Something weird happened.\n
                     %s
                     """ % e)
    except KeyError as e:
        raise KeyError(e)

    logger.debug("stop: counting +1s. Got %s.", result)
    return result
