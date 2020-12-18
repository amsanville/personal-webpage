from string import Template
# List of all webpages to be built in template
pages = [
    # Page 1: Welcome
    {
        'title' : 'Welcome',
        'file' : 'index.html',
        'navbar_title' : 'Home' 
    },
    # Page 2: About Me
    {
        'title' : 'Aboute Me',
        'file' : 'about.html',
        'navbar_title' : 'About' 
    },
    # Page 3: Portfolio
    {
        'title' : 'Portfolio',
        'file' : 'portfolio.html',
        'navbar_title' : 'Portfolio' 
    },
    # Page 4: Fun
    {
        'title' : 'Fun',
        'file' : 'fun.html',
        'navbar_title' : 'Fun' 
    }
]

blog_pages = [
    20201130,
    20201213,
    20201218
]

# Global storage for the links and titles
navbar_links = []
navbar_titles = []

def build_navbar():
    ''' Build Navbar
    Builds the navbar based on the list of pages provided at the top of this file.
    '''
    global pages, navbar_links, navbar_titles
    # Gather all the content for the navbar
    navbar_links = []
    navbar_titles = []
    for page in pages:
        navbar_links.append(page['file'])
        navbar_titles.append(page['navbar_title'])
    
    # Put blog last
    navbar_links.append('blog.html')
    navbar_titles.append('Blog')

def build_active(curr_page):
    ''' Build Active
    Create the list of strings for the navbar active tab highlighting
    curr_page - the file name of the current page linked in the navbar
    '''
    global navbar_links
    active = [''] * len(navbar_links)
    active[navbar_links.index(curr_page)] = 'active'
    return active

def build_page(title, content_file):
    ''' Build Page
    Builds the webpage based on the provided templates. Uses following template variables:
    title - the title of the webpage
    content_file - the html document for the content of the webpage, also the name of the html document output
    '''
    global navbar_links, navbar_titles

    # Load in the template
    template_text = open("./templates/template.html").read()
    template_obj = Template(template_text)

    # Load the content
    content = open("./content/" + content_file).read()

    # Choose which should be active
    active = build_active(content_file)

    # Use the template to build the website
    new_page = template_obj.safe_substitute(title = title, content = content,
        navbar_active_0 = active[0], navbar_page_0 = navbar_links[0], navbar_label_0 = navbar_titles[0],
        navbar_active_1 = active[1], navbar_page_1 = navbar_links[1], navbar_label_1 = navbar_titles[1],
        navbar_active_2 = active[2], navbar_page_2 = navbar_links[2], navbar_label_2 = navbar_titles[2],
        navbar_active_3 = active[3], navbar_page_3 = navbar_links[3], navbar_label_3 = navbar_titles[3],
        navbar_active_4 = active[4], navbar_page_4 = navbar_links[4], navbar_label_4 = navbar_titles[4])
    open('./docs/' + content_file, 'w+').write(new_page)

def build_blog_archive():
    ''' Build Blog Archive
    Builds the archive part of the blog
    '''
    archive = ''
    for entry in reversed(blog_pages):
        # Reconstruct the date
        day = entry % 100
        month = int(((entry % 10000) - day) / 100)
        year = int((entry - month * 100 - day) / 10000)

        # Create the string
        archive += '<a href=./blog_post_' + str(entry) + '.html>' + str(month) + '/' + str(day) + '/' + str(year) + '</a></br>'
    return archive

def build_blog():
    ''' Build Blog
    Builds the entire blog based on all entries
    '''
    global navbar_links, navbar_titles, blog_pages

    # Load in the template
    template_text = open('./templates/blog_base.html').read()
    template_obj = Template(template_text)

    # Build the archive part of the page
    archive = build_blog_archive()

    # Choose which should be active
    active = build_active('blog.html')

    # Build each entry
    for entry in blog_pages:
        # Load the last blog entry (i.e. the one with the largest date
        content = open('./blog/' + str(entry) + '.html').read()
        # Use the template to build the website
        new_page = template_obj.safe_substitute(title = 'Blog', content = content, archive = archive,
            navbar_active_0 = active[0], navbar_page_0 = navbar_links[0], navbar_label_0 = navbar_titles[0],
            navbar_active_1 = active[1], navbar_page_1 = navbar_links[1], navbar_label_1 = navbar_titles[1],
            navbar_active_2 = active[2], navbar_page_2 = navbar_links[2], navbar_label_2 = navbar_titles[2],
            navbar_active_3 = active[3], navbar_page_3 = navbar_links[3], navbar_label_3 = navbar_titles[3],
            navbar_active_4 = active[4], navbar_page_4 = navbar_links[4], navbar_label_4 = navbar_titles[4])

        # Write the page
        open('./docs/blog_post_' + str(entry) + '.html', 'w+').write(new_page)
    # Last entry and blog landing page are the same
    open('./docs/blog.html', 'w+').write(new_page)

def main():
    global pages
    # Initialize the builder
    # Based on the use of globals and initialize I would compartmentalize this into a class...
    # * pages would be a static variable
    # * navbar_links and titles would both be attributes built during initialization

    # Pre-processing for navbar
    build_navbar()
    # Pre-processing for blog
    blog_pages.sort()

    # Invoke build page a bunch of times
    print('Building Website')
    for page in pages:
        build_page(page['title'], page['file'])
    
    # Build the blog
    build_blog()

if __name__ == '__main__':
    main()