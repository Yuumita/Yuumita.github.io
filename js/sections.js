document.addEventListener("DOMContentLoaded", function () {
    const tableOfContentsContainer = document.getElementById("table-of-contents");
    const mainContent = document.querySelector(".article-content");

    const title = mainContent.querySelectorAll("h1")[0];
    const link = document.createElement("a");
    link.textContent = title.textContent;
    link.style = "font-size: 125%;";
    link.setAttribute("href", `#${title.id}`);
    tableOfContentsContainer.appendChild(link);

    const headings = mainContent.querySelectorAll("h3, h4");
    headings.forEach((heading) => {
        const link = document.createElement("a");

        link.textContent = heading.textContent;

        if(heading.nodeName == "H4") {
            link.style="margin-left: 1.5rem;";
        } else if(heading.nodeName == "H5") {
            link.style="margin-left: 3rem;";
        }

        link.setAttribute("href", `#${heading.id}`);
        tableOfContentsContainer.appendChild(link);
    });

    // Restart MathJax after updating html
    if(MathJax.typesetPromise) MathJax.typesetPromise();
});