package io.lecon.privatepunch

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.Bundle
import android.os.Handler
import android.support.v7.app.AppCompatActivity
import android.text.TextUtils
import android.util.Base64
import android.util.Log
import android.widget.Toast
import com.bumptech.glide.Glide
import com.google.gson.Gson
import kotlinx.android.synthetic.main.activity_login.*
import okhttp3.MediaType
import okhttp3.RequestBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory


class LoginActivity : AppCompatActivity() {

    private lateinit var service: Api


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)
        initComponent()
        showVerifyCode()
        next.setOnClickListener {
            val text = edit_code.text.toString()
            if (TextUtils.isEmpty(text)) {
                Toast.makeText(this@LoginActivity, "不能为空", Toast.LENGTH_LONG).show()
            }
            val reqBody = RequestBody.create(MediaType.parse("application/json; charset=utf-8"), Gson().toJson(ReqBean(text)))
            service.postVerifyCode(reqBody)
                    .enqueue(object : Callback<RespBean> {
                        override fun onFailure(call: Call<RespBean>, t: Throwable) {
                            hander.sendEmptyMessage(0)
                            t.printStackTrace()
                        }

                        override fun onResponse(call: Call<RespBean>, response: Response<RespBean>) {
                            hander.sendEmptyMessage(1)
                            Log.i(MainActivity.TAG, "resp :" + response.body())
                        }
                    })
        }

    }

    private val hander: Handler = Handler {
        when {
            it.what == 1 -> {
                Toast.makeText(this@LoginActivity, "成功！！！", Toast.LENGTH_LONG).show()
                true
            }
            it.what == 0 -> {
                Toast.makeText(this@LoginActivity, "失败", Toast.LENGTH_LONG).show()
                true
            }
            else -> {
                false
            }
        }
    }

    private fun initComponent() {
        val retrofit = Retrofit.Builder()
                .baseUrl("http://punch.leconio.com:8000/")
                .addConverterFactory(GsonConverterFactory.create())
                .build()


        service = retrofit.create(Api::class.java)
    }

    private fun showVerifyCode() {
        IMAGE?.let {
            val base64Img = it.img
            val bitmap = base64ToBitMap(base64Img)
            Glide.with(this)
                    .load(bitmap)
                    .into(verifyCode)

        }
    }


    companion object {
        var IMAGE: MsgExtra? = null
        /**
         * base64编码字符集转化成BitMap。
         */
        fun base64ToBitMap(base64Str: String): Bitmap {
            val imageByte = Base64.decode(base64Str, Base64.DEFAULT)
            return BitmapFactory.decodeByteArray(imageByte, 0, imageByte.size)
        }
    }

    data class ReqBean(var msg: String)
    data class RespBean(var msg: String)

}