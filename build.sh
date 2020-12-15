# Small change for git purposes.

# Build index
# Change the title
sed 's/${title}/Welcome/g' ./templates/template.html > ./docs/index.html

# Change the active flags
sed -i 's/${active_home}/active/' ./docs/index.html
sed -i 's/${active_about}//' ./docs/index.html
sed -i 's/${active_portfolio}}//' ./docs/index.html
sed -i 's/${active_blog}//' ./docs/index.html
sed -i 's/${active_fun}//' ./docs/index.html
sed -i 's/${active_test}//' ./docs/index.html

# Copy and paste the content page into the right location
sed -i '/${content}/r ./content/index.html' ./docs/index.html
sed -i 's/${content}//' ./docs/index.html

# Build about
# Change the title
sed 's/${title}/About/g' ./templates/template.html > ./docs/about.html

# Change the active flags
sed -i 's/${active_home}//' ./docs/about.html
sed -i 's/${active_about}/active/' ./docs/about.html
sed -i 's/${active_portfolio}}//' ./docs/about.html
sed -i 's/${active_blog}//' ./docs/about.html
sed -i 's/${active_fun}//' ./docs/about.html
sed -i 's/${active_test}//' ./docs/about.html

# Copy and paste the content page into the right location
sed -i '/${content}/r ./content/about.html' ./docs/about.html
sed -i 's/${content}//' ./docs/about.html

# Build portfolio
# Change the title
sed 's/${title}/Portfolio/g' ./templates/template.html > ./docs/portfolio.html

# Change the active flags
sed -i 's/${active_home}//' ./docs/portfolio.html
sed -i 's/${active_about}//' ./docs/portfolio.html
sed -i 's/${active_portfolio}}/active/' ./docs/portfolio.html
sed -i 's/${active_blog}//' ./docs/portfolio.html
sed -i 's/${active_fun}//' ./docs/portfolio.html
sed -i 's/${active_test}//' ./docs/portfolio.html

# Copy and paste the content page into the right location
sed -i '/${content}/r ./content/portfolio.html' ./docs/portfolio.html
sed -i 's/${content}//' ./docs/portfolio.html

# Build blog
# Change the title
sed 's/${title}/Blog/g' ./templates/template.html > ./docs/blog.html

# Change the active flags
sed -i 's/${active_home}//' ./docs/blog.html
sed -i 's/${active_about}//' ./docs/blog.html
sed -i 's/${active_portfolio}}//' ./docs/blog.html
sed -i 's/${active_blog}/active/' ./docs/blog.html
sed -i 's/${active_fun}//' ./docs/blog.html
sed -i 's/${active_test}//' ./docs/blog.html

# Copy and paste the content page into the right location
sed -i '/${content}/r ./content/blog.html' ./docs/blog.html
sed -i 's/${content}//' ./docs/blog.html

# Build fun
# Change the title
sed 's/${title}/Fun/g' ./templates/template.html > ./docs/fun.html

# Change the active flags
sed -i 's/${active_home}//' ./docs/fun.html
sed -i 's/${active_about}//' ./docs/fun.html
sed -i 's/${active_portfolio}}//' ./docs/fun.html
sed -i 's/${active_blog}//' ./docs/fun.html
sed -i 's/${active_fun}/active/' ./docs/fun.html
sed -i 's/${active_test}//' ./docs/fun.html

# Copy and paste the content page into the right location
sed -i '/${content}/r ./content/fun.html' ./docs/fun.html
sed -i 's/${content}//' ./docs/fun.html

# Build test
# Change the title
sed 's/${title}/Test/g' ./templates/template.html > ./docs/test.html

# Change the active flags
sed -i 's/${active_home}//' ./docs/test.html
sed -i 's/${active_about}//' ./docs/test.html
sed -i 's/${active_portfolio}}//' ./docs/test.html
sed -i 's/${active_blog}//' ./docs/test.html
sed -i 's/${active_fun}//' ./docs/test.html
sed -i 's/${active_test}/active/' ./docs/test.html

# Copy and paste the content page into the right location
sed -i '/${content}/r ./content/test.html' ./docs/test.html
sed -i 's/${content}//' ./docs/test.html
