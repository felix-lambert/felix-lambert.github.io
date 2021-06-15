---
layout: post
title: What is kotlin?
date: 2021-06-03 10:18:00
tags: technology
---

- [Kotlin](https://en.wikipedia.org/wiki/Kotlin_(programming_language))

Kotlin is a statically types open source programming language. The name comes from the Kotlin Island, near St. Petersburg. It runs on the Java/JVM virtual machine platform runtime code (compiling into Java bytecode), but also compiles to JavaScript (the current implementation of Kotlin/JS targets ES5) and you can also write apps that works in ios as well. 

The JVM is fundamentally a 32-bit machine. 

For the moment, kotlin is primarly being used for android. Google estimating that 70% of the top 1000 apps on the Play Store are written in Kotlin. Google itself has 60 apps written in Kotlin, including Maps and Drive. It's a language created by the people at JetBrains (formerly IntelliJ Software s.r.o.). 

Kotlin and coroutines >

Coroutines dramatically simplify background task management for everything from network calls to accessing local data.

```kotlin
suspend fun main() = coroutineScope {
    for (i in 0 until 10) {
        launch {
            delay(1000L - i * 10)
            print("$i ")
        }
    }
}
```

Kotlin and Object-oriented Hello

```kotlin
class Greeter(val name: String) {
    fun greet() {
        println("Hello, $name")
    }
}

fun main(args: Array<String>) {
    Greeter(args[0]).greet()
}
```

```kotlin
data class Product(val name: String, val price: Int)
fun List<Product>.checkOut() {
    val totalPrice = sumBy { it.price }
    val allPositions = joinToString(separator = " and ") { it.name }
    println("You've bought $allPositions for $totalPrice coins!")
}
```