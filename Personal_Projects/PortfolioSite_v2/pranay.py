#!/usr/bin/env python
#
# Copyright 2017 Pranay Marella
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#Base
import webapp2
from google.appengine.ext import ndb
from helpers import *

#Models
from models.categories import Categories
from models.comments import Comments
from models.like import Like
from models.projects import Projects
from models.skills import Skills
from models.status import Status
from models.user import User
from models.education import Education

#Handlers
from handlers.handler import Handler
from handlers.aboutmehandler import AboutMeHandler
from handlers.deletecategory import DeleteCategory
from handlers.deleteproject import DeleteProject
from handlers.editprojecthandler import EditProjectHandler
from handlers.filterprojects import FilterProjects
from handlers.frontpagehandler import FrontPageHandler
from handlers.login import Login
from handlers.logout import Logout
from handlers.mainpagehandler import MainPageHandler
from handlers.newsfeedhandler import NewsFeedHandler
from handlers.projectshandler import ProjectsHandler
from handlers.register import Register
from handlers.searchhandler import SearchHandler
from handlers.signup import Signup
from handlers.updatecategoryhandler import UpdateCategoryHandler
from handlers.updateprojecthandler import UpdateProjectHandler
from handlers.updateskillhandler import UpdateSkillHandler
from handlers.updatestatus import UpdateStatus
from handlers.visitmainhandler import VisitMainHandler
from handlers.visitprojectshandler import VisitProjectsHandler
from handlers.updateeducationhandler import UpdateEducationHandler
from handlers.deleteeducation import DeleteEducation
from handlers.filterotherprojects import FilterOtherProjects
from handlers.visitprofile import VisitProfileHandler

app = webapp2.WSGIApplication([('/', FrontPageHandler),
                               ('/logout', Logout),
                               ('/login', Login),
                               ('/signup', Register),
                               ('/main', MainPageHandler),
                               ('/UPHandler', UpdateProjectHandler),
                               ('/AddCategory', UpdateCategoryHandler),
                               ('/UpdateEducation', UpdateEducationHandler),
                               ('/AddSkill', UpdateSkillHandler),
                               ('/editproject/([0-9]+)', EditProjectHandler),
                               ('/Delete/([0-9]+)', DeleteProject),
                               ('/DeleteCategory/([0-9]+)', DeleteCategory),
                               ('/DeleteEducation/([0-9]+)', DeleteEducation),
                               ('/projects', ProjectsHandler),
                               ('/FilterProjects', FilterProjects),
                               ('/about_me', AboutMeHandler),
                               ('/newsfeed', NewsFeedHandler),
                               ('/updatestatus', UpdateStatus),
                               ('/search', SearchHandler),
                               ('/visit/([a-zA-Z0-9]+)',VisitMainHandler),
                               ('/visit/projects/([a-zA-Z0-9]+)', VisitProjectsHandler),
                               ('/visit/FilterProjects/([a-zA-Z0-9]+)', FilterOtherProjects),
                               ('/visit/profile/([a-zA-Z0-9]+)', VisitProfileHandler)],
                               debug = True)
