package io.lecon.privatepunch

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log
import android.widget.Toast
import cn.jpush.android.api.JPushInterface
import com.google.gson.Gson


class PushReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        when {
            intent?.action == "cn.jpush.android.intent.NOTIFICATION_RECEIVED" -> {
                val bundle = intent.extras
                val content = bundle?.getString(JPushInterface.EXTRA_ALERT)
                val title = bundle?.getString(JPushInterface.EXTRA_NOTIFICATION_TITLE)

                if (content == "新消息来了") {
                    val extras = bundle.getString(JPushInterface.EXTRA_EXTRA)
                    val msgExtra = Gson().fromJson(extras, MsgExtra::class.java)
                    msgExtra.title = title
                    msgExtra.alert = content
                    LoginActivity.IMAGE = msgExtra
                } else {
                    Toast.makeText(context, "成功打卡$title", Toast.LENGTH_LONG).show()
                }
            }
            JPushInterface.ACTION_NOTIFICATION_OPENED == intent?.action -> {
                Log.d(MainActivity.TAG, "用户点击打开了通知")
                val startIntent = Intent(context, LoginActivity::class.java)
                startIntent.flags = Intent.FLAG_ACTIVITY_NEW_TASK
                context?.startActivity(startIntent)
            }
            else -> {
                Log.d(MainActivity.TAG, "Unhandled intent - ")
            }
        }
    }
}