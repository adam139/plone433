function MarqueeV() {
  var e = document.getElementById("oRollV");
  var t = document.getElementById("oRollV1");
  var n = document.getElementById("oRollV2");

  if(n.offsetTop - e.scrollTop <= 0) {
	  e.scrollTop -= t.offsetHeight;
  } else {
	  e.scrollTop++;
  }
}
function MarqueeVs() {
	  var e = document.getElementById("sRollV");
	  var t = document.getElementById("sRollV1");
	  var n = document.getElementById("sRollV2");
	  if(n.offsetTop - e.scrollTop <= 0) {
		  e.scrollTop -= t.offsetHeight;
	  } else {
		  e.scrollTop++;
	  }
	}
function StartRollV() {
  var e = document.getElementById("oRollV");
  var t = document.getElementById("oRollV1");
  var n = document.getElementById("oRollV2");

  if(e) {
    if(parseInt(e.style.height, 10) >= n.offsetTop) {
    	e.style.height = n.offsetTop;
      return
    }
    n.innerHTML = t.innerHTML;
    var rollspeed = 50;
    var myInter;
    myInter = setInterval(MarqueeV, rollspeed);
    e.onmouseover = function() {
      clearInterval(myInter);
    };
    e.onmouseout = function() {
      myInter = setInterval(MarqueeV, rollspeed);
    }
  }
}
function StartRollVs() {
	  var e = document.getElementById("sRollV");
	  var t = document.getElementById("sRollV1");
	  var n = document.getElementById("sRollV2");

	  if(e) {
	    if(parseInt(e.style.height, 10) >= n.offsetTop) {
	    	e.style.height = n.offsetTop;
	      return
	    }
	    n.innerHTML = t.innerHTML;
	    var rollspeeds = 50;
	    var myInters;
	    myInters = setInterval(MarqueeVs, rollspeeds);
	    e.onmouseover = function() {
	      clearInterval(myInters);
	    };
	    e.onmouseout = function() {
	      myInters = setInterval(MarqueeVs, rollspeeds);
	    }
	  }
	}