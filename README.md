# SSR Group Civil — website

A complete static website with a charcoal-and-gold theme, transparent gold SSR logo, premium concept renders, seven interactive 3D viewers and the SSR Site Log tool.

## Publish using GitHub Pages

1. Extract the ZIP on your computer or phone.
2. Create a GitHub repository, or open your existing website repository. A public repository can use GitHub Pages with GitHub Free.
3. Choose **Add file → Upload files**. Upload the extracted contents, including `index.html`, `style.css`, `site.js`, all images and all viewer HTML files. Do not upload only the ZIP. Keep `index.html` directly in the repository root, not inside an extra folder.
4. Commit the files to the `main` branch. When updating an existing repository, review/merge the change into its publishing branch.
5. Open **Settings → Pages → Build and deployment**. Set **Source** to **Deploy from a branch**, select **main**, select **/(root)**, and save.
6. Wait for deployment to complete. GitHub shows the website address on the Pages settings screen.

The `.nojekyll` file is included for static hosting. No npm install, framework or build command is required. All individual files are below GitHub's browser upload limit. If your browser struggles with a large batch, upload in smaller batches or use GitHub Desktop.

Official guidance:
- https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Push using Git from an existing local repository

Copy the extracted files into your local website repository, review the changes, and run:

```sh
git add .
git commit -m "Update SSR Group Civil website"
git push origin main
```

For a new repository, first create it on GitHub and follow GitHub's displayed instructions to connect the local folder to that repository. No GitHub credentials are included in this download.

## Custom domain

No custom domain is automatically connected by this ZIP. Configure your chosen domain in GitHub Pages settings and use the DNS records GitHub specifies. Existing social-preview metadata, robots.txt and sitemap.xml refer to ssrgroupcivil.in, inherited from the supplied site. Update these to your final public domain if using another address.

## Included pages

- `index.html`: homepage, projects and render gallery
- `services.html`: seven service areas
- `projects.html`: project and concept portfolio
- `3d.html`: all seven interactive model links
- `contact.html`: enquiries through WhatsApp or email
- `site-log.html`: supplied daily progress report tool
- `viewer-*.html`: the seven supplied interactive models
- `ssr-logo-gold-transparent.png`: gold SSR logo with alpha transparency
- JPG/WebP images, `style.css`, and `site.js`

## Behaviour and requirements

Use a modern browser with WebGL for 3D. Some viewers and PDF functions load third-party libraries online; a live internet connection may be needed. The contact form prepares a WhatsApp/email message for the visitor to review and send. It does not submit to a server. The site assistant uses preset answers, not an AI API. The supplied Site Log stores reports on the current device; any optional remote polishing feature still requires its original separate configuration.

Concept renders are labelled as concepts, not completed-project photography. Real-time viewer graphics differ from the enhanced still images. The new logo is an AI-prepared transparent adaptation of the supplied mark, with a gold bridge for contrast on dark surfaces.

## Editing

Edit the HTML files directly. Shared styles are in `style.css`. Keep relative links and image filenames consistent so the site works under a GitHub project subdirectory.
