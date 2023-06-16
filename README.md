## Browser extension "Search with DWDS"


Work in progress on a browser extension which interacts with the German online dictionary [DWDS](https://www.dwds.de). This extension allows for add the DWDS to the list of search engines, forwarding selected text to the DWDS search page on right-click, and typing dwds in the address bar to show search tools and suggestions.


### Current status

- Add DWDS to the list of search engines
    - Firefox :heavy_check_mark:
    - Chromium :question: ("Some extensions can add search engines to Chrome")
- Select text + right-click and "search with DWDS"
    - Firefox :heavy_check_mark:
    - Chromium :heavy_check_mark:
- Omnibox, i.e. shortcuts in address bar (functionality present but may vary)
   - Firefox :heavy_check_mark:
   - Chromium :heavy_check_mark:


### Build process

1. Install [Node Version Manager](https://github.com/nvm-sh/nvm) (nvm)
2. Install web-ext: `npm i -g web-ext`
3. Run `build.sh`


### Publication


* [Firefox add-on page](https://addons.mozilla.org/firefox/addon/dwds/)
* [Publish to Webstore](https://developer.chrome.com/docs/webstore/publish/) & [Chrome Webstore search](https://chrome.google.com/webstore/category/extensions)
