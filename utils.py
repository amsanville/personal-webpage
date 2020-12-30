import glob
from jinja2 import Template

'''
TODO:
- Make blog builder
- Refactor blog/project_euler code -> Build page from a content_template
- Update documentation
- Command line argument input
'''


# Some notes:
# - Blog posts are stored in html files with numbers for the date: YYYYMMDD.html. This list should be the numeric value of the YYYYMMDD date, making them sortable.

def build_page_list():
    '''
    TODO
    Fills in the pages global variable based on the contents found in the content sub-directory. Creates all the information about the page for the Jinja 2 template in template.html.

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

def build_blog_list():
    '''
    TODO
    '''
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

    # Update the blog content file so it contains the archive
    # Open the template
    with open('./templates/content_templates/blog_base.html') as fi:
        template = Template(fi.read())
    # Open the newest blog post
    with open(blog_entries[0]['input_file']) as fi:
        content = fi.read()
    # Output it as the blog file
    with open('./content/blog.html', 'w+') as fo:
        fo.write(template.render({
            'archive' : archive,
            'content' : content,
        }))
    return (blog_entries, archive)

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
    

def build_blog(blog_entries, archive, navbar):
    '''
    TODO
    Builds the blog pages based on the blog_base.html template using Jinja 2
    '''
    # Open the blog page template
    with open('./templates/content_templates/blog_base.html') as fi:
        blog_template = Template(fi.read())

    # Open the page template
    template = Template(open('./templates/template.html').read())
    
    # Update the navbar
    index_blog = next(index for index, navitem in enumerate(navbar) if navitem['title'].lower() == 'blog')
    navbar[index_blog]['active'] = 'active'

    # Template each of the blog entries
    for entry in blog_entries:
        # Open the input file
        with open(entry['input_file']) as fi:
            content = fi.read()

        # Put the archive and content into the blog page template
        result = blog_template.render({
            'archive' : archive,
            'content' : content,
        })

        # Render the template
        result = template.render({
            'title' : 'Blog',
            'navbar' : navbar,
            'content' : result,
        })

        # Write the result
        with open(entry['output_file'], 'w+') as fo:
            fo.write(result)
    
    # Reset the navbar
    navbar[index_blog]['active'] = ''

def build_project_euler(navbar):
    '''
    Populates the list of Project Euler solutions based on what exists in the directories. Then updates the page linked to on the Fun page.
    '''
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
    # Now that we have a list of all the PDFs and python files and which problems they go to, feed them to the Jinja content template
    with open('./templates/content_templates/project_euler.html') as fi:
        template_pe = Template(fi.read())
    content_pe = template_pe.render({
        'solutions' : solutions
    })

    # Feed this content to the page template
    with open('./templates/template.html') as fi:
        template = Template(fi.read())
    
    # Set the fun tab to active in the navbar
    index_fun = next(index for index, navitem in enumerate(navbar) if navitem['title'].lower() == 'fun')
    navbar[index_fun]['active'] = 'active'
    
    # Template
    result = template.render({
            'title' : 'Project Euler',
            'navbar' : navbar,
            'content' : content_pe,
    })

    # Reset the navbar
    navbar[index_fun]['active'] = ''

    # Write to a new HTML file
    with open('./docs/project_euler.html', 'w+') as fo:
        fo.write(result)

def build_all():
    # Gather all the content page information
    (pages, navbar) = build_page_list()
    # Gather all the blog information and update the blog.html file
    (blog_entries, archive) = build_blog_list()
    # Build the pages
    build_pages(pages, navbar)
    # Build the individual blog entries
    build_blog(blog_entries, archive, navbar)
    # Create the list of blog entries
    build_project_euler(navbar)