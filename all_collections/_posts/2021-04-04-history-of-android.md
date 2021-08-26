---
layout: post
title: History of android
date: 2021-04-04 10:18:00
tags: technologie
---

Source: 
- [Good summary](https://www.youtube.com/watch?v=9wWgw9smBJs)
- [Oracle vs Google](https://www.youtube.com/watch?v=IDwGHr32Vw4)

Rubin described the Android project as having "tremendous potential in developing smarter mobile devices that are more aware of its owner's location and preferences". The early intentions of the company were to develop an advanced operating system for digital cameras, and this was the basis of its pitch to investors in April 2004. The company then decided that the market for cameras was not large enough for its goals, and five months later it had diverted its efforts and was pitching Android as a handset operating system that would rival Symbian and Microsoft Windows Mobile.

The Apple App store was launched on 10 July 2008 with 500 apps. The Google Play Store, which was originally known as the Android Market was launched on 22 October 2008.

In the summer of 2019, Huawei announced it would create an alternative operating system to Android known as Harmony OS, and has filed for intellectual property rights across major global markets. Huawei does not currently have any plans to replace Android in the near future, as Harmony OS is designed for internet of things devices, rather than for smartphones.

The main hardware platform for Android is ARM (the ARMv7 and ARMv8-A architectures), with x86 and x86-64 architectures also officially supported in later versions of Android.

Android is not Linux in the traditional Unix-like Linux distribution sense; Android does not include the GNU C Library (it uses Bionic as an alternative C library) and some other components typically found in Linux distributions. Android's standard C library, Bionic, was developed by Google specifically for Android, as a derivation of the BSD's standard C library code. Bionic itself has been designed with several major features specific to the Linux kernel. The main benefits of using Bionic instead of the GNU C Library (glibc) or uClibc are its smaller runtime footprint, and optimization for low-frequency CPUs. At the same time, Bionic is licensed under the terms of the BSD licence, which Google finds more suitable for the Android's overall licensing model.

In contrast to desktop Linux distributions, Android device owners are not given root access to the operating system and sensitive partitions such as /system/ are read-only. However, root access can be obtained by exploiting security flaws in Android, which is used frequently by the open-source community to enhance the capabilities and customizability of their devices, but also by malicious parties to install viruses and malware.

On top of the Linux kernel, there are the middleware, libraries and APIs written in C, and application software running on an application framework which includes Java-compatible libraries. 

Matthew Panzarino, co-editor of TechCrunch, believes that there are three phases of app history in mobile technology. Firstly, the initial gaming and utilities apps available in mobiles. This was seen in early PDAs and the first-generation iPhone. Secondly, apps that were focused around grabbing the user's attention and dominating the mobile home screen. Thirdly, today's phase in which apps are service layers, purpose built and utilise technology such as hardware sensors, location, history of use and predictive computation. Today in 2021 apps are not only present in technology such as mobiles and computers but also wearable technology such as watches.

Android is open source.

Diagram of android >

1. Linux Kernel
2. Hardware Abstraction Layer
3. Native Services
3. Runtime
4. Application Framework
5. Applications

The Application Framework is the API's that you touch in your app. Inside the android framework, you have the Manager and the Service (System Server) (Alarm, Notifications...) which is basically talking to hardware. 

The Application Manager and the System Server (Services) lives in different processes on the system. We need an inter process communication (IPC) to communicate. The thing in android is called Binder. Binder is a very low level API. So android decided to abstract it. The abstraction names are proxies and stubs (AIDL). We can pass objects through the binder IPC.

Service Manager > Every service are being called through the service manager by a name which is a string.

To see all the services in the device:

```
adb shell service list
```

All the informations of this list is handled by Service Manager.

When the app is being launched, all the services are being saved into the cache. The app touches for example the alarm manager (which is a proxy) that goes and get the alarm sercie through the IPC. Managers in general don't do a lot. They delegate that job to something else.

App-specific storage: storage only for your app. Prevents other app to use the data stored. If uninstalled, the data will be removed.

Shared storage: files that our app intends to share with other app. If uninstall, the data will not be removed.

Preferences: key-value pairs. If uninstalled, the data will be removed.

Databases: Room persistence library / sqlite. If uninstalled, the data will be removed. Room provides an abstraction over sqlite. Advantage: the user can still browse that content while they are offline. Any user-initiated content changes are then synced to the server when the device is online again.

In older Android Studio versions:

Emulator -> Android Studio -> Device File Explorer -> /data/data/{$packageId}/databases/ -> Save As -> https://sqlitebrowser.org/

In later Android Studio versions (3.5+):

View -> Tool Windows -> Device File Explorer -> /data/data/{$packageId}/databases/ -

Network storage: Firebase...

Intents are used to start a new activity.