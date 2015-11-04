'''
Defines the views of the user profile.
This defines the interaction points, but the actual logic is treated
by the :mod:`controller`.
'''
from flask import render_template, flash, redirect, url_for
from flask import Flask, jsonify, request, abort
from flask import current_app, Blueprint
from flask.ext.api import status 
from flask.helpers import make_response
from app import app, auth
import datetime
import json
import time
from lxml import objectify
from requests import ConnectionError

from app import controller

    