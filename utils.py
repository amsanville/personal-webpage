import glob
from jinja2 import Template

'''
TODO:
- Update README
- Command line argument input
'''


# Some notes:
# - Blog posts are stored in html files with numbers for the date: YYYYMMDD.html. This list should be the numeric value of the YYYYMMDD date, making them sortable.

def build_page_list():
    '''
    Creates a pages and navbar variables for the Jinja 2 template in template.html, returning the dictionaries in a tuple.

    Note, this function is specifically kepy separate from the build_pages() function in order to allow other functions to use it to gather the navbar information.

    Requires there to be content files:
    - index.html
    - about.html
    - blog.html
    Throws a FileNotFoundError if these files aren't found
    '''
    # Initialize output
    pages = []
    navbar = []
    # Check for the pages
    page_location = glob.glob("./content/*.html")
    # Check for the necessary content files
    if './content/index.html' in page_location and './content/about.html' in page_location and './content/blog.html' in page_location:
        # Turn the page location data into a file and title
        for index, page in enumerate(page_location, 0):
            # Pull out the name of the html files
            # Note: the ./content/ and .html are fixed so we can use a slice
            page_name = page[10:-5]
            # Create the dictionary entry for the page
            pages.append({
                'input_file' : page,
                'title' : page_name,
                'output_file' : f'./docs/{page_name}.html',
                })

        # Correct the order of the pages
        # -index (home), about, blog, then all others
        pages.insert(0, pages.pop(next(index for index, page in enumerate(pages) if page['input_file'] == './content/blog.html')))
        pages.insert(0, pages.pop(next(index for index, page in enumerate(pages) if page['input_file'] == './content/about.html')))
        pages.insert(0, pages.pop(next(index for index, page in enumerate(pages) if page['input_file'] == './content/index.html')))
        # Note: the next() function is used on iterables and can be used in the above way to make a more general index() function for lists than just equality comparison.
        # The above code pop's out the list item of interest and inserts it at the front of the list, so we do the pages in reverse order, putting blog in front, then about in front of blog, and finally index (the home page) in front
        
        # Finally, correct the index.html title
        pages[0]['title'] = 'Welcome'

        # Now that all the pages have been processed and properly ordered, we can fill in the info for the navbar
        for page in pages:
            navbar.append({
                'title' : page['title'],
                'url' : './' + page['output_file'][7:],
                'active' : '',
            })
    else:
        error_message = []
        # Throw a file not found error for the appropriate file(s)
        if './content/index.html' not in page_location:
            error_message.append('index.html')    
        if './content/about.html' not in page_location:
            error_message.append('about.html')  
        if './content/blog.html' not in page_location:
            error_message.append('blog.html')
        temp = ', '.join(error_message)         
        raise FileNotFoundError(f'Unable to find in {temp} in content sub-directory.')
    return (pages, navbar)

def build_pages(pages, navbar):
    '''
    Builds the webpages based on the template.html template using Jinja 2.
    '''
    template = Template(open('./templates/template.html').read())
    for index, page in enumerate(pages):
        # Set the active tab
        navbar[index]['active'] = 'active'

        # Read the content
        with open(page['input_file']) as fi:
            content = fi.read()

        # Render the template
        result = template.render({
            'title' : page['title'],
            'navbar' : navbar,
            'content' : content,
        })

        # Write the result
        with open(page['output_file'], 'w+') as fo:
            fo.write(result)

        # Reset the active tab
        navbar[index]['active'] = ''
    
def build_from_content_template(inner_file, inner_dict, outer_file, outer_dict, output_file):
    '''
    Uses secondary template to build the content of the primary template. Based on the pattern used in the blog posts and Project Euler stuff.

    inner_file - the file location of the inner template file
    inner_dict - the dictionary to be used in the jinja render statement
    outer_file - the file location of the outer template file, template should use the content key value appropriately
    outer_dict - the dictionary to be used in the jinja render statement, has inner content added to it as the content
    output_file - the location of the output file
    '''

    # Read in the inner template
    with open(inner_file) as fi:
        inner_template = Template(fi.read())

    # Read in the outer template
    with open(outer_file) as fi:
        outer_template = Template(fi.read())

    # Render the dictionaries in successive order with jinja
    outer_dict['content'] = inner_template.render(inner_dict)
    result = outer_template.render(outer_dict)

    # Write the result
    with open(output_file, 'w+') as fo:
        fo.write(result)

def build_blog():
    '''
    Builds the entire blog, including updating the main blog page to the most recent blog entry
    '''
    # Get the navbar information and set blog to active
    (_, navbar) = build_page_list()
    index_blog = next(index for index, navitem in enumerate(navbar) if navitem['title'].lower() == 'blog')
    navbar[index_blog]['active'] = 'active'

    blog_location = glob.glob("./blog/*.html")
    # Sort and reverse the list so the newest (i.e. largest date) is first
    blog_location.sort()
    blog_location.reverse()

    # Process out the entries
    blog_entries = []
    archive = []
    for blog_entry in blog_location:
        # Slice out the identifier entry
        blog_date = blog_entry[7:-5]
        output_file = f'./docs/post_{blog_date}.html'
        # Create an input and output file for the entry
        blog_entries.append({
                'input_file' : blog_entry,
                'title' : 'Blog',
                'output_file' : output_file,
                })
        
        # Append the output file to the archive
        archive.append({
            'date' : f'{blog_date[4:6]}/{blog_date[6:]}/{blog_date[0:4]}',
            'url' : f'./{output_file[7:]}',
        })

    # Gather the blog templates and jinja dicts updating the blog splash page
    inner_file = './templates/content_templates/blog_base.html'
    inner_dict = {
        'archive' : archive,
    }
    with open(blog_entries[0]['input_file']) as fi:
            inner_dict['content'] = fi.read()
    outer_file = './templates/template.html'
    outer_dict = {
        'title' : 'Blog',
        'navbar' : navbar
    }
    output_file = './docs/blog.html'
    build_from_content_template(inner_file, inner_dict, outer_file, outer_dict, output_file)

    # Build each other individual blog page
    for entry in blog_entries:
        # Update the content and write location
        with open(entry['input_file']) as fi:
            inner_dict['content'] = fi.read()
        output_file = entry['output_file']

        # Build the page
        build_from_content_template(inner_file, inner_dict, outer_file, outer_dict, output_file)
    
def build_project_euler():
    '''
    Populates the list of Project Euler solutions based on what exists in the directories. Then updates the page linked to on the Fun page.
    '''
    # Get the navbar information and set the fun tab to active
    (_, navbar) = build_page_list()
    index_fun = next(index for index, navitem in enumerate(navbar) if navitem['title'].lower() == 'fun')
    navbar[index_fun]['active'] = 'active'

    # Get the pdf and python files
    pdfs = glob.glob('./docs/project_euler/*.pdf')
    pdfs.sort()
    pys = glob.glob('./docs/project_euler/*.py')
    pys.sort()

    # Check through all the pdfs and pys pairing up those that are for the same problem
    # It's like the merge in merge sort
    index_pdfs = 0
    index_pys = 0
    pys_done = False
    pdfs_done = False
    solutions = []
    while not pys_done and not pdfs_done:
        # Check the problem number for the current file in each list
        if pdfs[index_pdfs][35:-4] == pys[index_pys][35:-3]:
            # If equal
            num = pdfs[index_pdfs][35:-4]
            solutions.append({
                'num' : num,
                'pdf' : f'project_euler_{num}.pdf',
                'py' : f'project_euler_{num}.py',
            })

            # Increment the PDF file index
            index_pdfs += 1
            if index_pdfs == len(pdfs):
                pdfs_done = True

            # Increment the python file index
            index_pys += 1
            if index_pys == len(pys):
                pys_done = True

        elif pdfs[index_pdfs][35:-4] < pys[index_pys][35:-3]:
            # If PDF has a lower problem number than the next python file
            num = pdfs[index_pdfs][35:-4]
            solutions.append({
                'num' : num,
                'pdf' : f'project_euler_{num}.pdf',
                'py' : None,
            })

            # Increment the PDF file index
            index_pdfs += 1
            if index_pdfs == len(pdfs):
                pdfs_done = True
        else:
            # If the python file has a lower problem number than the pdf
            num = pys[index_pdfs][35:-3]
            solutions.append({
                'num' : num,
                'pdf' : None,
                'py' : f'project_euler_{num}.py',
            })

            # Increment the python file index
            index_pys += 1
            if index_pys == len(pys):
                pys_done = True

    # Check which list finished first
    if pdfs_done and not pys_done:
        # Finish the rests of the python files
        while index_pys < len(pys):
            num = pys[index_pdfs][35:-3]
            solutions.append({
                'num' : num,
                'pdf' : None,
                'py' : f'project_euler_{num}.py',
            })

            # Increment the python file index
            index_pys += 1

    if pys_done and not pdfs_done:
        # Finish the rest of the PDF files
        while index_pdfs < len(pdfs):
            num = pdfs[index_pdfs][35:-4]
            solutions.append({
                'num' : num,
                'pdf' : f'project_euler_{num}.pdf',
                'py' : None,
            })

            # Increment the PDF file index
            index_pdfs += 1

    # Gather all the information
    inner_file = './templates/content_templates/project_euler.html'
    inner_dict = {'solutions' : solutions}
    outer_file = './templates/template.html'
    outer_dict = {
        'title' : 'Project Euler',
        'navbar' : navbar,
    }
    output_file = './docs/project_euler.html'

    # Build
    build_from_content_template(inner_file, inner_dict, outer_file, outer_dict, output_file)

def build_all():
    # Gather all the content page information
    (pages, navbar) = build_page_list()
    # Build the pages
    build_pages(pages, navbar)
    # Build the individual blog entries
    build_blog()
    # Create the list of blog entries
    build_project_euler()