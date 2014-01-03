import web
class IndexPage:
    def GET(self):
        render = web.template.render('templates')
        return render.index()


class UserPage:
    def GET(self):
        render = web.template.render('templates')
        return render.my()