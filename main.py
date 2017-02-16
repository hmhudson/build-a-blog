
import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class BlogPost(db.Model):
    title = db.StringProperty(required = True)
    post_input= db.StringProperty(required = True)
    created= db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):

    def get(self):
        posts= db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC LIMIT 5")
        self.render("homepage.html", posts = posts)

class NewPost(Handler):
    def render_newpost(self, title="", post_input="", error=""):
        self.render("new-post.html", title= title, post_input= post_input, error= error)

    def get(self):
        self.render_newpost()

    def post(self):
        title= self.request.get("title")
        post_input= self.request.get("post_input")

        if title and post_input:
            new_post= BlogPost(title= title, post_input= post_input)
            new_post.put()
            id = new_post.key().id()

            self.redirect("/blog/" + str(id))
        else:
            error= "We need a title and post!"
            self.render_newpost(title, post_input, error)

class ViewPostHandler(Handler):
    def get(self, id):
        post= BlogPost.get_by_id(int(id))
        self.render("individual_post.html", post= post)




app = webapp2.WSGIApplication([
    ('/blog', MainPage),
    ('/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
