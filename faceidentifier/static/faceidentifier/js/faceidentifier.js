let button = document.querySelector(".Ddtc");
let noti_green = document.querySelector(".noti-green");
let noti_red = document.querySelector(".noti-red");
let show = document.querySelector(".none");
let video;
let localstream;
let IDlop = document.querySelector("#IDLop").value;
const modal = document.getElementById("myModal");
const btn = document.getElementById("myBtn");
const modalcontent = document.querySelector(".modal-content1");
const noti_index = document.querySelector(".noti_index");
function beep() {
  var snd = new Audio("data:audio/wav;base64,//uQRAAAAWMSLwUIYAAsYkXgoQwAEaYLWfkWgAI0wWs/ItAAAGDgYtAgAyN+QWaAAihwMWm4G8QQRDiMcCBcH3Cc+CDv/7xA4Tvh9Rz/y8QADBwMWgQAZG/ILNAARQ4GLTcDeIIIhxGOBAuD7hOfBB3/94gcJ3w+o5/5eIAIAAAVwWgQAVQ2ORaIQwEMAJiDg95G4nQL7mQVWI6GwRcfsZAcsKkJvxgxEjzFUgfHoSQ9Qq7KNwqHwuB13MA4a1q/DmBrHgPcmjiGoh//EwC5nGPEmS4RcfkVKOhJf+WOgoxJclFz3kgn//dBA+ya1GhurNn8zb//9NNutNuhz31f////9vt///z+IdAEAAAK4LQIAKobHItEIYCGAExBwe8jcToF9zIKrEdDYIuP2MgOWFSE34wYiR5iqQPj0JIeoVdlG4VD4XA67mAcNa1fhzA1jwHuTRxDUQ//iYBczjHiTJcIuPyKlHQkv/LHQUYkuSi57yQT//uggfZNajQ3Vmz+Zt//+mm3Wm3Q576v////+32///5/EOgAAADVghQAAAAA//uQZAUAB1WI0PZugAAAAAoQwAAAEk3nRd2qAAAAACiDgAAAAAAABCqEEQRLCgwpBGMlJkIz8jKhGvj4k6jzRnqasNKIeoh5gI7BJaC1A1AoNBjJgbyApVS4IDlZgDU5WUAxEKDNmmALHzZp0Fkz1FMTmGFl1FMEyodIavcCAUHDWrKAIA4aa2oCgILEBupZgHvAhEBcZ6joQBxS76AgccrFlczBvKLC0QI2cBoCFvfTDAo7eoOQInqDPBtvrDEZBNYN5xwNwxQRfw8ZQ5wQVLvO8OYU+mHvFLlDh05Mdg7BT6YrRPpCBznMB2r//xKJjyyOh+cImr2/4doscwD6neZjuZR4AgAABYAAAABy1xcdQtxYBYYZdifkUDgzzXaXn98Z0oi9ILU5mBjFANmRwlVJ3/6jYDAmxaiDG3/6xjQQCCKkRb/6kg/wW+kSJ5//rLobkLSiKmqP/0ikJuDaSaSf/6JiLYLEYnW/+kXg1WRVJL/9EmQ1YZIsv/6Qzwy5qk7/+tEU0nkls3/zIUMPKNX/6yZLf+kFgAfgGyLFAUwY//uQZAUABcd5UiNPVXAAAApAAAAAE0VZQKw9ISAAACgAAAAAVQIygIElVrFkBS+Jhi+EAuu+lKAkYUEIsmEAEoMeDmCETMvfSHTGkF5RWH7kz/ESHWPAq/kcCRhqBtMdokPdM7vil7RG98A2sc7zO6ZvTdM7pmOUAZTnJW+NXxqmd41dqJ6mLTXxrPpnV8avaIf5SvL7pndPvPpndJR9Kuu8fePvuiuhorgWjp7Mf/PRjxcFCPDkW31srioCExivv9lcwKEaHsf/7ow2Fl1T/9RkXgEhYElAoCLFtMArxwivDJJ+bR1HTKJdlEoTELCIqgEwVGSQ+hIm0NbK8WXcTEI0UPoa2NbG4y2K00JEWbZavJXkYaqo9CRHS55FcZTjKEk3NKoCYUnSQ0rWxrZbFKbKIhOKPZe1cJKzZSaQrIyULHDZmV5K4xySsDRKWOruanGtjLJXFEmwaIbDLX0hIPBUQPVFVkQkDoUNfSoDgQGKPekoxeGzA4DUvnn4bxzcZrtJyipKfPNy5w+9lnXwgqsiyHNeSVpemw4bWb9psYeq//uQZBoABQt4yMVxYAIAAAkQoAAAHvYpL5m6AAgAACXDAAAAD59jblTirQe9upFsmZbpMudy7Lz1X1DYsxOOSWpfPqNX2WqktK0DMvuGwlbNj44TleLPQ+Gsfb+GOWOKJoIrWb3cIMeeON6lz2umTqMXV8Mj30yWPpjoSa9ujK8SyeJP5y5mOW1D6hvLepeveEAEDo0mgCRClOEgANv3B9a6fikgUSu/DmAMATrGx7nng5p5iimPNZsfQLYB2sDLIkzRKZOHGAaUyDcpFBSLG9MCQALgAIgQs2YunOszLSAyQYPVC2YdGGeHD2dTdJk1pAHGAWDjnkcLKFymS3RQZTInzySoBwMG0QueC3gMsCEYxUqlrcxK6k1LQQcsmyYeQPdC2YfuGPASCBkcVMQQqpVJshui1tkXQJQV0OXGAZMXSOEEBRirXbVRQW7ugq7IM7rPWSZyDlM3IuNEkxzCOJ0ny2ThNkyRai1b6ev//3dzNGzNb//4uAvHT5sURcZCFcuKLhOFs8mLAAEAt4UWAAIABAAAAAB4qbHo0tIjVkUU//uQZAwABfSFz3ZqQAAAAAngwAAAE1HjMp2qAAAAACZDgAAAD5UkTE1UgZEUExqYynN1qZvqIOREEFmBcJQkwdxiFtw0qEOkGYfRDifBui9MQg4QAHAqWtAWHoCxu1Yf4VfWLPIM2mHDFsbQEVGwyqQoQcwnfHeIkNt9YnkiaS1oizycqJrx4KOQjahZxWbcZgztj2c49nKmkId44S71j0c8eV9yDK6uPRzx5X18eDvjvQ6yKo9ZSS6l//8elePK/Lf//IInrOF/FvDoADYAGBMGb7FtErm5MXMlmPAJQVgWta7Zx2go+8xJ0UiCb8LHHdftWyLJE0QIAIsI+UbXu67dZMjmgDGCGl1H+vpF4NSDckSIkk7Vd+sxEhBQMRU8j/12UIRhzSaUdQ+rQU5kGeFxm+hb1oh6pWWmv3uvmReDl0UnvtapVaIzo1jZbf/pD6ElLqSX+rUmOQNpJFa/r+sa4e/pBlAABoAAAAA3CUgShLdGIxsY7AUABPRrgCABdDuQ5GC7DqPQCgbbJUAoRSUj+NIEig0YfyWUho1VBBBA//uQZB4ABZx5zfMakeAAAAmwAAAAF5F3P0w9GtAAACfAAAAAwLhMDmAYWMgVEG1U0FIGCBgXBXAtfMH10000EEEEEECUBYln03TTTdNBDZopopYvrTTdNa325mImNg3TTPV9q3pmY0xoO6bv3r00y+IDGid/9aaaZTGMuj9mpu9Mpio1dXrr5HERTZSmqU36A3CumzN/9Robv/Xx4v9ijkSRSNLQhAWumap82WRSBUqXStV/YcS+XVLnSS+WLDroqArFkMEsAS+eWmrUzrO0oEmE40RlMZ5+ODIkAyKAGUwZ3mVKmcamcJnMW26MRPgUw6j+LkhyHGVGYjSUUKNpuJUQoOIAyDvEyG8S5yfK6dhZc0Tx1KI/gviKL6qvvFs1+bWtaz58uUNnryq6kt5RzOCkPWlVqVX2a/EEBUdU1KrXLf40GoiiFXK///qpoiDXrOgqDR38JB0bw7SoL+ZB9o1RCkQjQ2CBYZKd/+VJxZRRZlqSkKiws0WFxUyCwsKiMy7hUVFhIaCrNQsKkTIsLivwKKigsj8XYlwt/WKi2N4d//uQRCSAAjURNIHpMZBGYiaQPSYyAAABLAAAAAAAACWAAAAApUF/Mg+0aohSIRobBAsMlO//Kk4soosy1JSFRYWaLC4qZBYWFRGZdwqKiwkNBVmoWFSJkWFxX4FFRQWR+LsS4W/rFRb/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////VEFHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAU291bmRib3kuZGUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMjAwNGh0dHA6Ly93d3cuc291bmRib3kuZGUAAAAAAAAAACU=");  
  snd.play();
}

//module dinh danh thu cong
button.onclick = () => {
  let SVTC = prompt("Nhập vào mã sinh viên");
  console.log(SVTC);
  let data = JSON.stringify(SVTC);
  const config = {
    method: "POST",
    url: "/faceidentifier/Manual/",
    headers: {
      //   'Authorization': 'Token c148eaabe85be02995148063c5c3b61dd1558a63',
      "Content-Type": "application/json",
    },
    data: data,
  };
  axios(config)
    .then(function (response) {
      console.log("success");
      console.log(response.data);
    })
    .catch(function (error) {
      console.log("pause");
      console.log(error);
    });
};
//tạo thông báo
function successalert(name) {
  let hello = document.querySelector(".hello");
  // hello.innerHTML = "Xin chào " + name;
  hello.innerHTML = "Định danh thành công";
  noti_green.onclick = function(){
    // alert('a');
    hello.innerHTML = "Xin chào " + name;
  }
  noti_green.style.display = "flex";
  setTimeout(function () {
    noti_green.style.display = "none";
  }, 5000);
}
function falsealert() {
  noti_red.style.display = "flex";
  setTimeout(function () {
    noti_red.style.display = "none";
  }, 5000);
}


// tạo video elment
function CreateVideo() {
  video = document.createElement("video");
  video.id = "video";
  // video.style.width = "100%";
  // video.style.height = "100%";
  video.setAttribute("autoplay", "autoplay");
  video.setAttribute("muted", "muted");
}

// load model
faceapi.nets.tinyFaceDetector.loadFromUri("/static/faceidentifier/js/models");
faceapi.nets.faceLandmark68Net.loadFromUri("/static/faceidentifier/js/models");
// faceapi.nets.ssdMobilenetv1.loadFromUri("/static/faceidentifier/js/models");
//đóng modal
function close_modal(video, localstream) {
  modal.style.display = "none";
  video.src = "";
  localstream.getTracks()[0].stop();
  console.log("Vid off");
  modalcontent.removeChild(video);
}

//module call api định danh khuôn mặt
function callapi(canvas) {
  let data = JSON.stringify(
    canvas.toDataURL("image/jpeg", 1.0).replace("data:image/jpeg;base64,", "")
  );
  const config = {
    method: "POST",
    url: "/faceidentifier/faceidentifier/",
    headers: {
      //   'Authorization': 'Token c148eaabe85be02995148063c5c3b61dd1558a63',
      "Content-Type": "application/json",
    },
    data: data,
  };
  axios(config)
    .then(function (response) {
      successalert(response.data);
      video.pause();
      beep();
      setTimeout(async () => {
        video.play();
      }, 6000);

      console.log(response.data);
    })
    .catch(function (error) {
      falsealert();
      video.pause();
      beep();
      setTimeout(async () => {
        video.play();
      }, 6000);
      // console.log("pause");
      // console.log(error);
    });
}

//onclick to show modal
btn.onclick = function () {
  modal.style.display = "block";
  CreateVideo();
  modalcontent.appendChild(video);
  if (navigator.mediaDevices.getUserMedia !== null) {
    var options = {
      video: true,
      audio: false,
    };
    navigator.webkitGetUserMedia(
      options,
      function (stream) {
        video.srcObject = stream;
        localstream = stream;
        console.log("streaming");
      },
      function (e) {
        console.log("background error : " + e.name);
      }
    );
  }
  // crop face image
  async function detec() {
    let detections = await faceapi.detectAllFaces(
      video,
      new faceapi.TinyFaceDetectorOptions()
    ).withFaceLandmarks();
    if (detections == undefined || detections.length != 1 ||detections[0].detection._score < 0.85) {
      noti_index.innerHTML = "Di chuyển mặt vào camera"
      setTimeout(async () => {
        detec();
        console.log('call back')
      }, 500);
    } else {
      noti_index.innerHTML = "Đang Định Danh"
      console.log(detections)
      console.log(detections.length)
      setTimeout(async () => {
        //extract face
        const regionsToExtract = [
          new faceapi.Rect(
            detections[0].detection.box.x,
            detections[0].detection.box.y,
            detections[0].detection.box.width,
            detections[0].detection.box.width
          ),
        ];
        let faceImages = await faceapi.extractFaces(video, regionsToExtract);
        faceImages.forEach((cnv) => {
          let canvas = document.createElement("canvas");
          canvas.width = "140";
          canvas.height = "140";
          let ctx = canvas.getContext("2d");
          ctx.drawImage(cnv, 0, 0, canvas.width, canvas.height);
          //myfunc(canvas,i)
          if(modal.style.display != "none"){
            callapi(canvas);

          }
        });
      }, 5000);
    }
  }
// lắng nghe sự kiện video bật
  video.addEventListener("play", async () => {
    noti_index.innerHTML = "Di chuyển mặt vào camera"
    await detec();
  });
  // close modal khi kích vào vùng trống hoặc nút hủy
  let close = document.querySelector(".close");
  close.onclick = () => {
    close_modal(video, localstream);
  };
  window.onclick = function (event) {
    if (event.target == modal) {
      close_modal(video, localstream);
    }
  };
};

// function logFromPython(){
//   pyscript.interpreter.interface.runPython(`
//       animal = "Python"
//       sound = "sss"
//       console.warn(f"{animal}s go " + sound * 5)
//   `)
// }

// logFromPython
