var FPS = 29.97;
var currentFrames = 0;


$(document).ready(function () {
    var currentFrame = $('#frame_count');
    var timeCode = $('#time_code');
    var fps = $('#fps')

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
        update_track_frame()
    })
})

function update_track_frame() {
    $.ajax({
        url: Flask.url_for('get_frame', {frame_id: video.get()}),
        type: "GET",
        success: function (response) {
            const format = (str2Format, ...args) => str2Format.replace(/(\{\d+\})/g, a => args[+(a.substr(1, a.length - 2)) || 0]);
            $("#myImage").attr('src', format("data:image/png;base64,{0}", response))
        },
        error: function (xhr) {
            console.log(xhr)
        }
    })
}

var clickCounter = 0;

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

function get_current_frame() {
    return Math.round(video.currentTime * FPS);
}