var startResults = 5;
var numResults = startResults;
var incResults = 5;

var selected_loc_filters = []
var selected_uni_filters = []
var searchTerm = ''
let tableVisible = false; 
let globalDoc = []; 
window.showTable = showTable; 

var docDiv = (doc) => {
    const name = doc[0];
    const prev = doc[1];
    const email = doc[2];
    const uni_dept = doc[4]+', '+doc[3]
    const fac_name = doc[5]
    const fac_url = doc[6]
    const loc = doc[7]+', '+doc[8]
    const queryText = doc[9] 
    const topics = doc[10]

    let randomNum = getRandomInt(5); 
    console.log(randomNum); 
    console.log(topics[randomNum]); 
    console.log(topics); 
    globalDoc.push(doc); 
    let docNum = globalDoc.indexOf(doc) + 1; 
    let divNum  = "div" + docNum; 
    let infoNum = "info" + docNum; 
    console.log(docNum); 


    console.log(fac_name);

    let info_id = ""; 
    if(fac_name == "") {
        console.log(true); 
        info_id = "no_name_email_info"
    } else {
        info_id = "no_email_info"
    }
    


    if (email =='None') {
        return (
             `<div class="card">
             <div class="card-header">
       <div style="display: flex;">

        
                 <b style="font-size:14pt">${fac_name}</b>
                 <a style="color:black;margin-left:auto;" onclick='showTable(this.id)' id=${infoNum}><i class="material-icons" id=${info_id}>info</i></a>
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
            <div style="margin-top:20px" id=${divNum}> 
            </div>`
        );
    } else {
        return (
            `<div class="card">
             <div class="card-header">
       <div style="display: flex;">

        
                 <b style="font-size:14pt">${fac_name}</b>
                 <a style="margin-left:auto;color:black;margin-right:20px;" href='mailto:${email}?subject=Request to Connect for conversation about Research&body=Dear Professor ${fac_name.split(" ")[1]}, %0D%0A %0D%0A It’s a pleasure to have gone through some of your research articles. I’d like to connect with you for discussing some ideas in the Research Area of ${topics[randomNum].charAt(0).toUpperCase() + topics[randomNum].slice(1)}. I hope to hear from you soon'"><i class="material-icons">email</i></a>
                 <a style="auto;color:black;margin-right:20px;" onclick="showTable(this.id)" id=${infoNum}><i class="material-icons">info</i></a>
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
            
            <div style="margin-top:20px" id=${divNum}> 
            </div>`
        );
    }
}

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

var showTable = function(clicked_id) {

    let id = parseInt(clicked_id.replace ( /[^\d.]/g, '' ));
    let doc = globalDoc[id-1]; 
    let email = doc[2];
    let uni_dept = doc[4]+', '+doc[3]
    let fac_name = doc[5];
    let topics = doc[10]; 
    let div = "div" + id; 

    let top5topics = []; 
    for(let i = 0; i < 5; i++) {
        let splitStr = topics[i].toLowerCase().split(' ');
        let myTopic = ""; 
        for (var x = 0; x < splitStr.length; x++) {
            splitStr[x] = splitStr[x].charAt(0).toUpperCase() + splitStr[x].substring(1);     
        }

        for(var x = 0; x < splitStr.length; x++) {
            myTopic += splitStr[x] + " "; 
        } 

        top5topics[i] = myTopic; 
    }

    if(tableVisible == false) { 
        tableVisible = true; 
    } else {
        tableVisible = false; 
    }

    if(tableVisible == true) {  
        var table = document.createElement("div");
        var c, r, t;
        t = document.createElement('table');
        t.setAttribute("id", "myTable");
        r = t.insertRow(0); 
        c = r.insertCell(0);
        c.innerHTML = "Topic 1";
        c = r.insertCell(1);
        c.innerHTML = "Topic 2";
        c = r.insertCell(2);
        c.innerHTML = "Topic 3";
        c = r.insertCell(3);
        c.innerHTML = "Topic 4";
        c = r.insertCell(4);
        c.innerHTML = "Topic 5";
        
        r = t.insertRow(1);
        c = r.insertCell(0);
        c.innerHTML = top5topics[0];
        addLearnMore(c, top5topics[0]); 
        addToQuery(c, top5topics[0]); 

        c = r.insertCell(1);
        c.innerHTML = top5topics[1];        
        addLearnMore(c, top5topics[1]); 
        addToQuery(c, top5topics[1]); 

        c = r.insertCell(2);
        c.innerHTML = top5topics[2];
        addLearnMore(c, top5topics[2]); 
        addToQuery(c, top5topics[2]); 

        c = r.insertCell(3);
        c.innerHTML = top5topics[3];
        addLearnMore(c, top5topics[3]); 
        addToQuery(c, top5topics[3]); 

        c = r.insertCell(4);
        c.innerHTML = top5topics[4];
        addLearnMore(c, top5topics[4]); 
        addToQuery(c, top5topics[4]); 


        // var node = document.createTextNode("This is new.");
        table.appendChild(t);
        var element = document.getElementById(div);
        element.appendChild(table);

        var table = document.getElementById("myTable").createCaption();
        table.innerHTML = "<b>Research Topics</b>";


    } else {
        let item = document.getElementById("myTable"); 
        item.parentNode.removeChild(item);
 
    }
}

var addLearnMore = function(c, topics) {
    var topicSplit  = topics.split(" "); 
    if (topicSplit[1] != null) {
        c.innerHTML += "</br>" + "<a  target='_blank' href='"+"https://en.wikipedia.org/wiki/"+ topicSplit[0] + "_" + topicSplit[1] +"'>Learn More</a>";
    } else {
        c.innerHTML += "</br>" + "<a  target='_blank' href='"+"https://en.wikipedia.org/wiki/"+ topicSplit[0] +"'>Learn More</a>";
    }


}

var addToQuery = function(c, topics) {
    var topicSplit  = topics.split(" ");
    console.log(topics); 
    c.innerHTML += "<button class='button' id='topic_cloud' type='button' onclick='addTopicToQuery(\""+topics+"\");'> Add to Query </button>";
}

function addTopicToQuery(topics) {
    console.log(topics); 
    numResults = startResults; 
    console.log(numResults); 
    searchTerm = $('#query').val() + " " + topics.toLowerCase(); 
    document.getElementById("query").value = searchTerm; 
    console.log(searchTerm);
    doSearch();
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