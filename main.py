
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

class MainPage(Handler):
    def get(self):
        self.render("homepage.html")

class NewPost(Handler):
    def render_newpost(self, title="", post_input="", error=""):
        self.render("new-post.html", title= title, post_input= post_input, error= error)


    def get(self):
        self.render_newpost()

    def post(self):
        title= self.request.get("title")
        post_input= self.request.get("post_input")

        if title and post_input:
            self.write("Thanks!")
        else:
            error= "We need a title and post!"
            self.render_newpost(title, post_input, error)


app = webapp2.WSGIApplication([
    ('/blog', MainPage),
    ('/newpost', NewPost)
], debug=True)
