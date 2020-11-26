var startResults = 5;
var numResults = startResults;
var incResults = 5;

var selected_loc_filters = []
var selected_uni_filters = []
var searchTerm = ''
let tableVisible = false; 

let fac_name = ""; 
let uni_dept = ""; 
let email = ""; 

var docDiv = (doc) => {
    const name = doc[0];
    const prev = doc[1];
    email = doc[2];
    uni_dept = doc[4]+', '+doc[3]
    fac_name = doc[5]
    const fac_url = doc[6]
    const loc = doc[7]+', '+doc[8]
    const queryText = doc[9] 



    if (email =='None') {
        return (
             `<div class="card">
             <div class="card-header">
       <div style="display: flex;">

        
                 <b style="font-size:14pt">${fac_name}</b>
                 <a style="color:black;margin-left:auto;" onclick="showTable('div2')"><i class="material-icons">info</i></a>
                 <a style="margin-left:auto;color:black;" href=${fac_url} target="_blank"><i class="material-icons">launch</i></a>
                 </div>

            <div class="header-item">
            <div class="tag">
            <i class='fas fa-university' ></i>
                  ${uni_dept}
            </div>
                <div class="tag">
                  <i class="material-icons">location_on</i>
                   ${loc}
                 </div>
            </div>
            </div>
           

              <div class="card-body">
                <span id='docPrev-${name}'>${prev}</span>
                <br>
            </div>
            </div>
            <div style="margin-top:20px" id="div2"> 
            </div>`
        );
    } else {
        return (
            `<div class="card">
             <div class="card-header">
       <div style="display: flex;">

        
                 <b style="font-size:14pt">${fac_name}</b>
                 <a style="margin-left:auto;color:black;margin-right:20px;" href='mailto:${email}' "><i class="material-icons">email</i></a>
                 <a style="auto;color:black;margin-right:20px;" onclick="showTable('div1')"><i class="material-icons">info</i></a>
                 <a style="color:black;" href=${fac_url} target="_blank"><i class="material-icons">launch</i></a>
                 </div>

            <div class="header-item">
            <div class="tag">
            <i class='fas fa-university' ></i>
                  ${uni_dept}
            </div>
                <div class="tag">
                  <i class="material-icons">location_on</i>
                   ${loc}
                 </div>
            </div>
            </div>
         

              <div class="card-body">
                <span id='docPrev-${name}'>${prev}</span>
                <br>
            </div>
            </div> 
            
            <div style="margin-top:20px" id="div1"> 
            </div>`
        );
    }
}

var showTable = function(div) {
    if(tableVisible == false) { 
        tableVisible = true; 
    } else {
        tableVisible = false; 
    }

    if(tableVisible == true) {  
        console.log("we will show the table now"); 
        var table = document.createElement("div");
        var c, r, t;
        t = document.createElement('table');
        console.log(div); 
        t.setAttribute("id", "myTable");
        r = t.insertRow(0); 
        c = r.insertCell(0);
        c.innerHTML = "First Name";
        c = r.insertCell(1);
        c.innerHTML = "Last Name";
        c = r.insertCell(2);
        c.innerHTML = "Department";
        c = r.insertCell(3);
        c.innerHTML = "Research Area";
        c = r.insertCell(4);
        c.innerHTML = "Email";
        
        r = t.insertRow(1);
        c = r.insertCell(0);
        c.innerHTML = fac_name;
        c = r.insertCell(1);
        c.innerHTML = fac_name;
        c = r.insertCell(2);
        c.innerHTML = uni_dept;
        c = r.insertCell(3);
        c.innerHTML = uni_dept;
        c = r.insertCell(4);
        c.innerHTML = email;


        // var node = document.createTextNode("This is new.");
        table.appendChild(t);
        var element = document.getElementById(div);
        element.appendChild(table);
    } else {
        let item = document.getElementById("myTable"); 
        item.parentNode.removeChild(item);
 
    }
}

var doSearch = function() {
    const data = {
        "query": searchTerm,
        "num_results": numResults,
        "selected_loc_filters" : selected_loc_filters,
        "selected_uni_filters": selected_uni_filters
    }
    if (searchTerm!='')
    {
    var num_fetched_res = 0
    fetch("http://localhost:8095/search", {
    // fetch("http://expertsearch.centralus.cloudapp.azure.com/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    }).then(response => {
        response.json().then(data => {
            const docs = data.docs;
            $("#docs-div").empty();

            docs.forEach(doc => {
            
                $("#docs-div").append(
                    docDiv(doc)
                );
                    num_fetched_res = num_fetched_res+1;

            });
          
            if (num_fetched_res==numResults){

            $("#loadMoreButton").css("display", "block")
        }
        else{
            $("#loadMoreButton").css("display", "none")
        }
        if (num_fetched_res==0){
            $("#docs-div").append(`<h3 style="text-align: center;margin-top:20px;">No Search Results Found</h3>`);
        }
        })

    });
}
}

$(window).on("resize",function() {
    $(document.body).css("margin-top", $(".navbar").height()+5 );
    var width = $(".select2-container").width()
    if ((width == 0)||width===undefined){
        width = 300
    }
    $(".select2-search__field").css('cssText', $(".select2-search__field").attr('style')+'width: ' + width+ 'px !IMPORTANT;');
}
).resize();


$(document).ready(function() {
    $('#loc_filter').select2({placeholder: "e.g. United States, California"});
    $('#uni_filter').select2({placeholder: "e.g. Stanford University"});
    $(window).trigger('resize');
});

window.onload=function(){
    for (var i=0;i<unis.length;i++){
         var newOption = new Option(unis[i], i, false, false);
        // Append it to the select
        $('#uni_filter').append(newOption).trigger('change');
       

    }
    selected_uni_filters = unis.slice()
    for (var i=0;i<locs.length;i++){
         var newOption = new Option(locs[i], i, false, false);
        // Append it to the select
        $('#loc_filter').append(newOption).trigger('change');
    }
    selected_loc_filters = locs.slice()
    $(window).trigger('resize');
 
};

function  toggleFilter() {
  filters_div = document.getElementById("search-filters")
  filters_div.style.display = filters_div.style.display=== 'none' ? 'flex' : 'none';
}

$("#submitButton").click(function() {
    numResults = startResults;
    searchTerm = $('#query').val()
    doSearch();
});

$("#filterButton").click(function() {
    toggleFilter();
});

$('#query').keydown(function(e) {
    searchTerm = $('#query').val()
    if (e.keyCode == 13) {
        numResults = startResults;
    
    doSearch();
    }
});

$("#applyFilters").click(function() {
  
    var selected_uni_data = $("#uni_filter").select2("data");
    selected_uni_filters = []
    selected_uni_data.forEach(s => {
            selected_uni_filters.push(s['text']);

});
      
    if (selected_uni_filters.length== 0){
        selected_uni_filters = unis.slice()
    }

    var selected_loc_data = $("#loc_filter").select2("data");
    selected_loc_filters = []
    selected_loc_data.forEach(s => {
            selected_loc_filters.push(s['text']);

});

    if (selected_loc_filters.length == 0){
        selected_loc_filters = locs.slice()
    }
  filters_div = document.getElementById("search-filters")
  filters_div.style.display = 'none'
        doSearch();
    });

$("#settingsButton").click(function() {
   window.location = "http://localhost:8095/admin"
});

$("#loadMoreButton").click(function() {
    numResults += incResults

    doSearch();
});