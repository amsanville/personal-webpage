from string import Template

def build_page(title, content_file, active):
    ''' Build Page

    Builds the webpage based on the provided templates. Uses following template variables:
    title - webpage title
    active_* - active or '' depending on whether the page is the appropriate one on the navbar
    content - the content of the page

    title - the title of the webpage
    content - the html document for the content of the webpage, also the name of the html document output
    active - list of strings (6) for the class in the navbar 'active' for navbar highlighting '' for inactive navbar order is the same as appears in the navbar
    '''
    # Load in the template
    template_text = open("./templates/template.html").read()
    template_obj = Template(template_text)

    # Load the content
    content = open("./content/" + content_file).read()

    # Use the template to build the website
    new_page = template_obj.safe_substitute(title = title, content = content,
        active_home = active[0],
        active_about = active[1], 
        active_portfolio = active[2], 
        active_blog = active[3], 
        active_fun = active[4], 
        active_test = active[5])
    open('./docs/' + content_file, 'w+').write(new_page)

if __name__ == '__main__':
    print('Building Website')
    build_page('Welcome', 'index.html', ['active', '', '', '', '', ''])
    build_page('About Me', 'about.html', ['', 'active', '', '', '', ''])
    build_page('Portfolio', 'portfolio.html', ['', '', 'active', '', '', ''])
    build_page('Portfolio', 'blog.html', ['', '', '', 'active', '', ''])
    build_page('Portfolio', 'fun.html', ['', '', '', '', 'active', ''])
    build_page('Portfolio', 'test.html', ['', '', '', '', '', 'active'])