function getTags() {

    // Assuming you want to fetch the articles in JSON format
    const postsFolderPath = "/articles/";
    return fetch(postsFolderPath + "articles.json")
        .then(response => response.json())
        .then(articles => {

            let articlesByTags = {};

            articles.forEach(article => {
                for(let index in article.tags) {
                    let tag = article.tags[index]
                    if(!(tag in articlesByTags)) articlesByTags[tag] = [];
                    articlesByTags[tag].push(article);
                }
            });

            return articlesByTags

        })
        .catch(error => console.error("Error fetching articles:", error));
}

async function fetchArticlesList() {
    const articlesListElement = document.getElementById("articles");

    articlesByTags = await getTags();

    for(let tag in articlesByTags) {

        const category = document.createElement("div");
        category.id = tag;
        articlesListElement.append(category)

        const categoryHeader = document.createElement("h2");
        categoryHeader.innerHTML = tag;
        category.appendChild(categoryHeader)


        const unorderedList = document.createElement("ul")
        unorderedList.id = tag + "-list"
        category.append(unorderedList)

        for(let article of articlesByTags[tag]) {
            const listItem = document.createElement("li");
            listItem.innerHTML = `${article.date} - <a href="${article.url}">${article.title}</a>`
            unorderedList.appendChild(listItem);
        }
    }

    // Restart MathJax after updating html
    if(MathJax.typesetPromise) MathJax.typesetPromise();
    
}

// Call the function to fetch the articles list immediately after the script is loaded
fetchArticlesList();
