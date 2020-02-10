/*
Create a menu item for the search engine
*/
function createMenuItem(engines) {
  browser.menus.create({
    id: "dwds",
    title: "im DWDS suchen",
    contexts: ["selection"]
  });
}

browser.search.get().then(createMenuItem);

/*
Search using the search engine whose name matches the
menu item's ID.
*/
browser.menus.onClicked.addListener((info, tab) => {
  browser.search.search({
    query: info.selectionText,
    engine: "DWDS"
  });
});