// Get Search Form and Page Links
let searchForm = document.getElementById('searchForm');
console.log(searchForm);
let pageLinks = document.getElementsByClassName('btn');

// Ensure search form exists
if (searchForm) {
    for (let i = 0; pageLinks.length > i; i++) {
        pageLinks[i].addEventListener('click', function (e) {
            e.preventDefault();

            // Get the Data attribute
            let page = this.dataset.page;

            // console.log('PAGE: ', page);

            //Add hidden Search Input to Form
            searchForm.innerHTML += `<input value=${page} name="page" hidden/>`;

            // Submit Form
            searchForm.submit();

        });
    }
}



