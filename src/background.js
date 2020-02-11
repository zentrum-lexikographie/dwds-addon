// display text according to current locale
var menuText = browser.i18n.getMessage("menuContent");
var omniboxSuggestion = browser.i18n.getMessage("omniboxSuggestion");
var omniboxText = browser.i18n.getMessage("omniboxText");

// construct queries starting from this URL
const baseURL = "https://www.dwds.de/wb/";


/*
Create a menu item for the search engine
*/
function createMenuItem(engines) {
  browser.menus.create({
    id: "dwds",
    title: menuText,
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


/*
Use omnibox to trigger DWDS query on user's request
*/
function getSuggestions(input) {
  var result = [];
  let suggestion = {
    content: baseURL + input,
    description: omniboxText
  }
  result.push(suggestion);
  return result;
}

browser.omnibox.setDefaultSuggestion({
  description: omniboxSuggestion
});

browser.omnibox.onInputChanged.addListener((input, suggest) => {
  suggest(getSuggestions(input));
});

browser.omnibox.onInputEntered.addListener((url, disposition) => {
  switch (disposition) {
    case "currentTab":
      browser.tabs.update({url});
      break;
    case "newForegroundTab":
      browser.tabs.create({url});
      break;
    case "newBackgroundTab":
      browser.tabs.create({url, active: false});
      break;
  }
});
