Information about page:
- Currently used theme: https://github.com/mmistakes/minimal-mistakes

Steps to execute when running after a long time. 
- Check jekyll current version: `bundle exec jekyll -v`
- Update jekyll to latest version: `gem update jekyll`
- Update theme to latest version: `bundle update` and update `remote_theme` in `_config.yml` to `mmistakes/minimal-mistakes@4.26.2`. The last part is the latest version number. 
- Run the website locally: `bundle exec jekyll serve`
- Push to changes to github: `git commit -a -m <message>` followed by `git push`

Steps to update the webpage: