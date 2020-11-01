var FPS = 29.97;
var currentFrames = 0;

let selectedFile;

$('#fileList a').on('click', function (e) {
    if (selectedFile !== this.getAttribute("index")) {
        e.preventDefault()
        $("#video_player").html('<source src="../static/uploads/' + this.getAttribute('fileName') + '.' + this.getAttribute("extension") + '"' + 'type="video/mp4"></source>');
        $("#video_player")[0].load()

        $('#previewWrapper').removeClass('d-none')
        $("#spinner").removeClass('d-none')
        $("#selectFileAlert").addClass('d-none')

        $("#propertiesFileAlert").addClass('d-none')
        $('#propertiesWrapper').removeClass('d-none')

        $('#defaultPropertiesBtn').removeAttr('disabled')
        $('#saveProperties').removeAttr('disabled')

        selectedFile = this.getAttribute("index")
    }

    update_track_frame()
    enableDeleteButton()
})

var mppRangeVal = $('#mppRange').val()
var fdRangeVal = $('#fdRange').val()

$(document).ready(function () {
    var currentFrame = $('#frame_count');
    var timeCode = $('#time_code');
    var fps = $('#fps')

    $('#mppDisplay').text(mppRangeVal)
    $('#fdDisplay').text(fdRangeVal)

    video = VideoFrame({
        id: 'video_player',
        frameRate: FrameRates.film,
        callback: function (frame) {
            currentFrame.html(frame);
            timeCode.html(video.toSMPTE())
            fps.html(video.frameRate)
        }
    });

    video.listen('frame');

    $('#retrieve').click(function () {
        $("#spinner").addClass('d-none')
        update_track_frame()
    })
})

function update_track_frame() {
    $.ajax({
        url: Flask.url_for('get_frame', {frame_id: video.get()}),
        type: "GET",
        context: this,
        success: function (response) {
            const format = (str2Format, ...args) => str2Format.replace(/(\{\d+\})/g, a => args[+(a.substr(1, a.length - 2)) || 0]);
            $("#myImage").attr('src', format("data:image/png;base64,{0}", response))
            $("#spinner").addClass('d-none')
        },
        error: function (xhr) {
            console.log(xhr)
        }
    })
}

function seekForward(nr_of_frames, fps) {
    if (video.paused == false) {
        video.pause();
    }

    video.seekForward(1, function () {
        console.log(video.get())
    });
}

function seekBackward(nr_of_frames, fps) {
    if (video.paused == false) {
        video.pause();
    }

    video.seekBackward(1, function () {
        console.log(video.get())
    });
}

function getRadius() {
    return fdRangeVal / 2.0 / mppRangeVal
}

function setRadiusDisplay() {
    $('#radiusDisplay').text(Math.round((getRadius() + Number.EPSILON) * 100) / 100)
}

$('#mppRange').on('input', function () {
    mppRangeVal = $('#mppRange').val()
    $('#mppDisplay').text(mppRangeVal)
    setRadiusDisplay()
})

$('#fdRange').on('input', function () {
    fdRangeVal = $('#fdRange').val()
    $('#fdDisplay').text(fdRangeVal)
    setRadiusDisplay()
})

$('#saveProperties').click(function () {
    let properties = {
        "mpp": mppRangeVal,
        "fd": fdRangeVal
    }

    $.ajax({
        url: Flask.url_for('save_properties'),
        type: "POST",
        data: JSON.stringify(properties),
        contentType: "application/json",
        context: this,
        success: function (response) {
            $('#propertiesSavedStatus').text('Saved')
        },
        error: function (xhr) {
            console.log(xhr)
        }
    })
})