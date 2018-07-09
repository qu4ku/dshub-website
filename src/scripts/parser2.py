"""

"""

import os
import django
from django.conf import settings

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils.dateparse import parse_date
from django.utils.text import slugify

import sys
# sys.path.append("..")
# sys.path.append('../project/settings')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'local')
# django.setup()


# from .models import Post, Feed, Tag, OtherTag
from core.models import Post, Feed, Tag, OtherTag

from bs4 import BeautifulSoup
from datetime import datetime
import feedparser
from hashlib import md5
import pandas as pd

from core.views import run_view
# Parser
def run():
	run_view(None, is_standalone=True)