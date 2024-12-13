import React from 'react'
import ReactPlayer from 'react-player'

function VideoPlayer() {
    return (
        <ReactPlayer url="/videos/HappyPeople.mp4" height="100%" width='100%' muted={true} loop={true} playing={true}/>
    )
}

export default VideoPlayer;