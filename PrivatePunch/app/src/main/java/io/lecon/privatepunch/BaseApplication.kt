package io.lecon.privatepunch

import android.app.Application
import cn.jpush.android.api.JPushInterface

class BaseApplication: Application() {
    override fun onCreate() {
        super.onCreate()
        JPushInterface.setDebugMode(true)    // 设置开启日志,发布时请关闭日志
        JPushInterface.init(this)            // 初始化 JPush
    }
}