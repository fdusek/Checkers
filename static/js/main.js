function initBoard(boardData, boardSize){
	$("#chessboard").empty();
	table = "<tbody>";
    var fieldClass;
    var fieldData;
    var table;
    for (x = 0; x < boardSize; x++) {
        table += "<tr class='_x" + x + "'>";
        for (y = 0; y < boardSize; y++) {
            fieldClass = "";
            fieldData = "";
            if (boardData[x] != undefined && boardData[x][y] != undefined) {
                fieldClass = boardData[x][y]["type"];
                fieldData = JSON.stringify(boardData[x][y]["next_moves"]);
            }

            table += "<td data-nextmoves='" + fieldData + "' class='_y" + y + " _x" + x + "'><span class='" + fieldClass + "'></span></td>";
        }
        table += "</tr>";
    }

	table += "</tbody>";
    var board = $("#chessboard");
	board.append(table);
	setBoardSize(board);
}

function setBoardSize(board){
	board.css('width', '');
	board.css('height', '');
	board.width((board.height()/100)*75);
	board.height(board.width());

	var fieldSize = board.find("td").width();
	board.find("span.piece").width((fieldSize/100)*80);
	board.find("span.piece").height((fieldSize/100)*80);

	board.find("span.piece").css("margin", (fieldSize/100)*10+"px");	
}

function boardToJson(){
	var result = {}
	$( "#chessboard").find("tr" ).each(function( index ) {
		$(this).children("td").each(function (index){
			var currentCoord = getCoordFromClasses($(this).attr('class').split(/\s+/));
			var x = currentCoord[0]
			var y = currentCoord[1]
			var piece = $(this).children("span.piece").first()
			if (piece.length){
				if(result[x] == undefined) {
					result[x] = {}
				}

				result[x][y] = {"type": piece.attr("class")};
			}
		})
	});
	return result;
}

function submitBoard(){
	jQuery.ajax ({
		url: "solve",
		type: "POST",
		data: JSON.stringify(boardToJson()),
		dataType: "json",
		contentType: "application/json; charset=utf-8",
		error: function(){ alert("Oops, there was a server error. Game was lost."); },
		success: function(data){
			console.log("Receiving data");
			console.log(JSON.stringify(data));
			initBoard(data, 8);
			subscribeEvents($('#chessboard'));
		}
	});
}

function getCoordFromClasses(classes){
    var x = 0;
    var y = 0;
	for (var index = 0; index < classes.length; ++index) {
    	if (classes[index].startsWith("_x")){
    		x = classes[index].replace("_x", "");
    	}
    	if (classes[index].startsWith("_y")){
    		y = classes[index].replace("_y", "");
    	}
	}
	return [x, y];
}



function subscribeEvents(board){
	$("html").click(
		function (){
			$("td").removeClass("move-possible move-selected");
		});

	board.find("td").click(
		function (){
			var currentCoord;
			var selectedCoord;
			var nextmoves;
			var highlight;
			var coord;
			if ($(this).hasClass("move-possible")) {
				currentCoord = getCoordFromClasses($(this).attr('class').split(/\s+/));
				selectedCoord = getCoordFromClasses($(".move-selected").attr('class').split(/\s+/));
				nextmoves = $("._x" + selectedCoord[0] + "._y" + selectedCoord[1]).data("nextmoves");

				for (var index = 0; index < nextmoves.length; ++index) {
					if (currentCoord.toString() == nextmoves[index].end_coord.toString()) {
						console.log("submiting node");
                        console.log(JSON.stringify(nextmoves[index]["next_state"]));
                        console.log("");
						initBoard(nextmoves[index].next_state, 8);
						subscribeEvents($("#chessboard"));
						submitBoard();
					}
				}

			} else {
				board.find("td").removeClass("move-selected move-possible");
				highlight = $(this).data("nextmoves");
				if (Boolean(highlight)) {
					$(this).addClass("move-selected");
					for (var i = 0; i < highlight.length; i++) {
						coord = highlight[i]["end_coord"];
						board.find("._x" + coord[0] + "._y" + coord[1]).addClass("move-possible");
					}
				} else {
					board.find("td").removeClass("move-selected move-possible");
				}
			}
			event.stopPropagation();
		});
	

	board.find("td").hover(
		function(){
			highlight = $(this).data("nextmoves");
			if (Boolean(highlight)){
				for (var i=0; i < highlight.length; i++) {
					coord = highlight[i]["end_coord"];
					board.find("._x" + coord[0] + "._y" + coord[1]).addClass("highlight-hover");
				}		
			}
	},
		function(){
			$("#chessboard").find("td").removeClass("highlight-hover");
		} 
	)
}

board = {};
boardSize = 8;


$( document ).ready(function() {
	$.getJSON("/new", function(data) {
	    initBoard(data, 8);
	    subscribeEvents($("#chessboard"));
	});
});