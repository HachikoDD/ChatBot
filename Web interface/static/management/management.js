function CreateTableFromJSON() {
    var myBooks = [
        {
          "id": "5d3c6547f05fd2a88037bb1c",
          "Question": "How do I initialize the weights when I train a deep neural network?"
        },
        {
          "id": "5d3c6547f05fd2a88037bb1c",
          "Question": "Learn how to add a class name to an element with JavaScript."
        },
        {
          "id": "5d3c6547f05fd2a88037bb1c",
          "Question": "At W3Schools you will find complete references about tags, attributes, events, color names, entities, character-sets, URL encoding, language codes, HTTP messages, and more."
        },
        {
          "id": "5d3c6547f05fd2a88037bb1c",
          "Question": "The perfect solution for professionals who need to balance work, family, and career building."
        },{
          "id": "5d3c6547f05fd2a88037bb1c",
          "Question": "How do I initialize the weights when I train a deep neural network?"
        },
        {
          "id": "5d3c6547f05fd2a88037bb1c",
          "Question": "Learn how to add a class name to an element with JavaScript."
        },
        {
          "id": "5d3c6547f05fd2a88037bb1c",
          "Question": "At W3Schools you will find complete references about tags, attributes, events, color names, entities, character-sets, URL encoding, language codes, HTTP messages, and more."
        },
        {
          "id": "5d3c6547f05fd2a88037bb1c",
          "Question": "The perfect solution for professionals who need to balance work, family, and career building."
        },{
          "id": "5d3c6547f05fd2a88037bb1c",
          "Question": "How do I initialize the weights when I train a deep neural network?"
        },
        {
          "id": "5d3c6547f05fd2a88037bb1c",
          "Question": "Learn how to add a class name to an element with JavaScript."
        },
        {
          "id": "5d3c6547f05fd2a88037bb1c",
          "Question": "At W3Schools you will find complete references about tags, attributes, events, color names, entities, character-sets, URL encoding, language codes, HTTP messages, and more."
        },
        {
          "id": "5d3c6547f05fd2a88037bb1c",
          "Question": "The perfect solution for professionals who need to balance work, family, and career building."
        }
    ]

    // EXTRACT VALUE FOR HTML HEADER.
    // ('Book ID', 'Book Name', 'Category' and 'Price')
    var col = [];
    for (var i = 0; i < myBooks.length; i++) {
        for (var key in myBooks[i]) {
            if (col.indexOf(key) === -1) {
                col.push(key);
            }
        }
    }

    // ADD JSON DATA TO THE TABLE AS ROWS.
    for (var i = 0; i < myBooks.length; i++) {
        for (var j = 1; j < col.length; j++) {
            AddOneRow(myBooks[i][col[j]]);
        }
    }
}

// AddOneRow("ne success getFullYear");
function AddOneRow(content) {
    var content = content;

    var row = "";
    row += '<tr class ="zA"><td class ="question">' + content +'</td></tr>';

    // get the current table body html as a string, and append the new row
    var html = document.getElementById("contenttable_tbody").innerHTML + row;

    // set the table body to the new html code
    document.getElementById("contenttable_tbody").innerHTML = html;
}
