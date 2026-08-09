package com.example.twofun_app

import android.app.Activity
import android.os.Bundle
import android.widget.TextView

class MainActivity : Activity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val textView = TextView(this)
        textView.text = "NATIVE ANDROID TEST"
        textView.textSize = 24f

        setContentView(textView)
    }
}
