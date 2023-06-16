/**
 * Some functionality can be used the same way with both API's!
 * Firefox and Safari: browser
 * Chrome, Opera, Edge: chrome
 * See https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Build_a_cross_browser_extension
 */
const isFirefox = (typeof browser === 'object')
const pluginApi = (isFirefox ? browser : chrome)
const contextMenu = isFirefox ? browser.menus : chrome.contextMenus

// display text according to current locale
const menuText = pluginApi.i18n.getMessage("menuContent")
const omniboxSuggestion = pluginApi.i18n.getMessage("omniboxSuggestion")
const omniboxText = pluginApi.i18n.getMessage("omniboxText")

// construct queries starting from this URL
const baseURL = "https://www.dwds.de/?q="
const suggestionBaseURL = "https://www.dwds.de/wb/typeahead?q="

/*
 Actions to execute only when the add-on is installed or updated
 See https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/runtime/onInstalled
 */
pluginApi.runtime.onInstalled.addListener(() => {
  /*
   Create a contextmenu entry and tell the browser to show this entry only when text is selected.
   See https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/menus/create
   */
  contextMenu.create({
    id: "dwds",
    title: menuText,
    contexts: ["selection"]
  })
})


/*
When the contextmenu item is clicked:
In Firefox -> search using the search engine with name "DWDS" declared in the manifest
In Chrome -> create a new tab with the URL of DWDS (since in Chrome no engine can be selected)
See https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/menus/onClicked
*/
contextMenu.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'dwds') {
    if (isFirefox) {
      browser.search.search({
        query: info.selectionText,
        engine: "DWDS"
      })
    } else {
      chrome.tabs.create({url: baseURL + info.selectionText})
    }
  }
})


/*
Set the default suggestion description
See https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/omnibox/setDefaultSuggestion
*/
pluginApi.omnibox.setDefaultSuggestion({
  description: omniboxSuggestion
})


async function getSuggestions(input) {
  const result = []
  await fetch(suggestionBaseURL + input)
    .then(res => res.json())
    .then(res => {
      for (const suggestion of res) {
        result.push({
          content: baseURL + suggestion.value,
          description: `${suggestion.value}`
        })
      }
    }).catch(console.error)

    return result
}


/*
See https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/omnibox/onInputChanged
 */
pluginApi.omnibox.onInputChanged.addListener(async (input, suggest) => {
  suggest(await getSuggestions(input))
})

/*
See https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/omnibox/onInputEntered
 */
pluginApi.omnibox.onInputEntered.addListener((url, disposition) => {
  if (!url.startsWith(baseURL)) {
    url = baseURL + url
  }
  switch (disposition) {
    case "currentTab":
      pluginApi.tabs.update({url})
      break
    case "newForegroundTab":
      pluginApi.tabs.create({url})
      break
    case "newBackgroundTab":
      pluginApi.tabs.create({url, active: false})
      break
  }
})
