function fetchArticlesList() {
    const articlesListElement = document.getElementById("articles-list");

    // Assuming the "posts" folder is at the root of the website
    const postsFolderPath = "/articles/";

    // Assuming you want to fetch the articles in JSON format
    fetch(postsFolderPath + "articles.json")
        .then(response => response.json())
        .then(articles => {
            articles.forEach(article => {
                const listItem = document.createElement("li");
                listItem.innerHTML = `${article.date} - <a href="${article.url}">${article.title}</a>`
                articlesListElement.appendChild(listItem);
            });
            // Restart MathJax after updating html
            if(MathJax.typesetPromise) MathJax.typesetPromise();
        })
        .catch(error => console.error("Error fetching articles:", error));
}

// Call the function to fetch the articles list immediately after the script is loaded
fetchArticlesList()