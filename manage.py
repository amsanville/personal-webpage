import utils
import sys

def print_commands():
    '''
    Prints out the extra command line functionality and what it is meant to do.
    '''
    print('build - rebuilds all content')
    print('blog - rebuilds blog')
    print('euler - rebuilds project euler solutions list')
    print('new - creates a new content page to fill in')

def main():
    '''
    Runs the SSG
    '''

    # See if there are commands to process
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'build':
            utils.build_all()
        elif command == 'blog':
            utils.build_blog()
        elif command == 'euler':
            utils.build_project_euler()
        elif command == 'new':
            with open('new.html', 'w+') as fo:
                fo.write('''
                    <h1>New Content!</h1>

                    <p>New content...and your navbar probably looks weird...</p>
                '''.replace('    ', ''))
        else:
            print('Unrecognized command. Valid commands:')
            print_commands()
    else:
        # If not
        print('Valid commands:')
        print_commands()
    
if __name__ == '__main__':
    main()