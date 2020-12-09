---
layout: post
title: How does react-native works?
date: 2019-10-15 10:18:00
tags: technology
---

SOURCE:

- [React native bridge](https://subscription.packtpub.com/book/application_development/9781787282537/1/01lvl1sec9/how-the-react-native-bridge-from-javascript-to-native-world-works)
- [https://reactnative.dev/docs/communication-ios](https://reactnative.dev/docs/communication-ios)
- [https://facebook.github.io/react-native/](https://facebook.github.io/react-native/)
- [https://en.wikipedia.org/wiki/React_Native](https://en.wikipedia.org/wiki/React_Native)
- [https://www.youtube.com/watch?v=qSRrxpdMpVc&t=231s](https://www.youtube.com/watch?v=qSRrxpdMpVc&t=231s)
- [https://www.youtube.com/watch?v=rReCzR6DMEM](https://www.youtube.com/watch?v=rReCzR6DMEM)
- [https://github.com/jondot/rn-snoopy](https://github.com/jondot/rn-snoopy)
- [https://blog.logrocket.com/overcoming-single-threaded-limitations-in-react-native/](https://blog.logrocket.com/overcoming-single-threaded-limitations-in-react-native/)
- [https://reactnative.dev/docs/performance](https://reactnative.dev/docs/performance)
- [https://stackoverflow.com/questions/53588142/the-benefits-of-react-native-javascriptcore](https://stackoverflow.com/questions/53588142/the-benefits-of-react-native-javascriptcore)
- [https://stackoverflow.com/questions/33479180/what-does-react-native-use-to-allow-javascript-to-be-executed-on-ios-and-android](https://stackoverflow.com/questions/33479180/what-does-react-native-use-to-allow-javascript-to-be-executed-on-ios-and-android)
- [https://www.freecodecamp.org/news/how-react-native-constructs-app-layouts-and-how-fabric-is-about-to-change-it-dd4cb510d055/](https://www.freecodecamp.org/news/how-react-native-constructs-app-layouts-and-how-fabric-is-about-to-change-it-dd4cb510d055/)
- [https://www.reactnative.guide/3-react-native-internals/3.1-react-native-internals.html](https://www.reactnative.guide/3-react-native-internals/3.1-react-native-internals.html)
- [https://www.youtube.com/watch?time_continue=1&v=0MlT74erp60&feature=emb_logo](https://www.youtube.com/watch?time_continue=1&v=0MlT74erp60&feature=emb_logo)
- [https://www.youtube.com/watch?time_continue=1&v=8N4f4h6SThc&feature=emb_logo](https://www.youtube.com/watch?time_continue=1&v=8N4f4h6SThc&feature=emb_logo)
- [https://www.youtube.com/watch?time_continue=3&v=UcqRXTriUVI&feature=emb_logo](https://www.youtube.com/watch?time_continue=3&v=UcqRXTriUVI&feature=emb_logo)
- [https://levelup.gitconnected.com/wait-what-happens-when-my-react-native-application-starts-an-in-depth-look-inside-react-native-5f306ef3250f](https://levelup.gitconnected.com/wait-what-happens-when-my-react-native-application-starts-an-in-depth-look-inside-react-native-5f306ef3250f)
- [https://www.raywenderlich.com/1227-javascriptcore-tutorial-for-ios-getting-started](https://www.raywenderlich.com/1227-javascriptcore-tutorial-for-ios-getting-started)
- [https://www.youtube.com/watch?v=\_IiDHmAPH28](https://www.youtube.com/watch?v=_IiDHmAPH28)

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/view.png)</span>

# Let's understand what happens when a user starts running a react-native app

To run the application one of the following commands is issued via the command-line interface (CLI): `react-native run-ios` or `react-native run-android`


- This command runs at the native entry point thread (native thread) on which your Android (Java/Kotlin) or IOS (Swift/Objective C) app is running. This thread is automatically assigned by the phone’s operating system.

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/process.png)</span>

The native thread (or main thread) has access to what the user is seeing. All events (touch event, timer event, network request event...) are listened on the native side.

- The command creates a RootView (RCTRootView) that gives everything visible to the user.

- The RootView creates the Bridge Interface.

The Bridge takes care of the communication by serializing it through JSON messages (on the native side and on the JavaScript side) so that it can pass across. This communication is actually quite similar to a client (native thread) and a server (JS thread).

- The Bridge Interface will send messages to create the JavaScript (JS) thread to execute the code that is written in react-native.

- Once the Bridge passes serialized payload to JavaScript, Event is processed and your application logic comes into play.

Like all JavaScript virtual machines, this JS thread is an event loop where your react application lives, API calls are made, touch events are interpreted, etc. It will start loading JS bundles into a single main.bundle.js file by compiling it into EcmaScript 5 using babel (Babel JavaScript compiler).

- When React starts rendering it sends the changes to another thread: the Shadow thread.

React-native uses flexbox to style and position the elements in the screen. But the native UI has his own layout system so it does not understand flexbox. This is why react-native has created his own library called yoga to translate the flexbox css to the mobile layout.

The shadow thread is like a mathematical engine which finally decides on how to compute the view positions in a tree of nodes, like the html.

<span style="display:block;text-align:center"> <img src="{{site.baseurl}}/assets/img/native.png" alt="drawing" width="900"/></span>

Let's look at this code as an example:

```jsx let d const App = props = { return ( <View> <Text>Hello there</Text> </View> ) }

```

If the JS thread wants a view and text to be created it will batch the request into a single message and send it across to the shadow thread to interpret the positions for the native thread. Then the message will be rendered to the Native thread to render the the UI.

`<View />` or `<TextInput />` or `<Text/>` are special components compiled into native code. The `<View>` component will be linked to android.view for android and UIView for ios. `<TextInput>` will be linked to EditText for android and UITextField for IOS.

- Since only the main thread is able to render something on the screen, shadow thread should send generated layout to the main thread, and only then UI renders.