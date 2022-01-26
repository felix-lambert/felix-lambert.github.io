---
layout: post
title: Work environment > EmptyMyFridge
date: 2022-01-06 10:18:00
tags: application
---

A developer using the managed workflow doesn't use Xcode or Android Studio, they just write JavaScript code and manage configuration for things like the app icon and splash screen through app.json. The Expo SDK exposes an increasingly comprehensive set of APIs that give you the power to access device capabilities like the camera, biometric authentication, file system, haptics, and so on.

When you run expo start (or npm start), Expo CLI starts Metro Bundler, which is an HTTP server that compiles the JavaScript code of our app using Babel and serves it to the Expo app. It also pops up Expo Dev Tools, a graphical interface for Expo CLI.

Our text is black and small. We should change the color because, according to some folks, you should never use pure black for text or backgrounds. We'll also increase the font size to make it easier to read.

An "asset" is any file that your project uses that is not code. Images, videos, sounds, and fonts are all considered to be assets.

ResizeMode, an image style property that lets us control how the image is resized to fit the given dimensions.

To keep context re-rendering fast, React needs to make each context consumer a separate node in the tree.

React Native doesn't have a built-in API for navigation like a web browser does. React Navigation provides this for you, along with the iOS and Android gestures and animations to transition between screens.

If you run this code, you'll notice that when you tap "Go to Details... again" that it doesn't do anything! This is because we are already on the Details route. The navigate function roughly means "go to this screen", and if you are already on that screen then it makes sense that it would do nothing.

Let's suppose that we actually want to add another details screen. This is pretty common in cases where you pass in some unique data to each route (more on that later when we talk about params!). To do this, we can change navigate to push. This allows us to express the intent to add another route regardless of the existing navigation history.

When you call navigate it first tries to find an existing route with that name, and only pushes a new route if there isn't yet one on the stack.

Nested navigators don't receive parent's events​

For example, if you have a stack navigator nested inside a tab navigator, the screens in the stack navigator won't receive the events emitted by the parent tab navigator such as (tabPress) when using navigation.addListener.

To receive events from parent navigator, you can explicitly listen to parent's events with navigation.getParent():

```javascript
const unsubscribe = navigation.getParent().addListener('tabPress', (e) => {
  // Do something
});
```

If you want to create separate group of screens for organization, instead of using separate navigators, you can use the Group component.

NavigationContainer is a component which manages our navigation tree and contains the navigation state. This component must wrap all navigators structure. Usually, we'd render this component at the root of our app, which is usually the component exported from App.js.

The state of a navigator generally looks something like this:

```javascript
{
  key: 'StackRouterRoot',
  index: 1,
  routes: [
    { key: 'A', name: 'Home' },
    { key: 'B', name: 'Profile' },
  ]
}
```

For this navigation state, there are two routes (which may be tabs, or cards in a stack). The index indicates the active route, which is "B".

While React Native exports a SafeAreaView component, it has some inherent issues, i.e. if a screen containing safe area is animating, it causes jumpy behavior. In addition, this component only supports iOS 10+ with no support for older iOS versions or Android. We recommend to use the react-native-safe-area-context library to handle safe areas in a more reliable way.

Don't wrap your whole app in SafeAreaView, instead wrap content inside your screens.

useNavigation is a hook which gives access to the navigation object. It's useful when you cannot pass the navigation prop into the component directly, or don't want to pass it in case of a deeply nested child.

Parent's useEffect/componentDidMount is always called after child's useEffect/componentDidMount.

There are few properties present in every navigation state object:

type - Type of the navigator that the state belongs to, e.g. stack, tab, drawer.
key - Unique key to identify the navigator.
routeNames - Name of the screens defined in the navigator. This is an unique array containing strings for each screen.
routes - List of route objects (screens) which are rendered in the navigator. It also represents the history in a stack navigator. There should be at least one item present in this array.
index - Index of the focused route object in the routes array.
history - A list of visited items. This is an optional property and not present in all navigators. For example, it's only present in tab and drawer navigators in the core. The shape of the items in the history array can vary depending on the navigator. There should be at least one item present in this array.
stale - A navigation state is assumed to be stale unless the stale property is explicitly set to false. This means that the state object needs to be "rehydrated".

The Link component lets us navigate to a screen using a path instead of a screen name based on the linking options. It preserves the default behavior of anchor tags in the browser such as Right click -> Open link in new tab", Ctrl+Click/⌘+Click etc.

Following are the built-in events available with every navigator:

focus - This event is emitted when the screen comes into focus

blur - This event is emitted when the screen goes out of focus

beforeRemove - This event is emitted when the user is leaving the screen, there's a chance to prevent the user from leaving

state (advanced) - This event is emitted when the navigator's state changes

Inside a screen, you can add listeners on the navigation prop with the addListener method. The addListener method takes 2 arguments: type of the event, and a callback to be called on the event. It returns a function that can be called to unsubscribe from the event.

Example:

```javascript
const unsubscribe = navigation.addListener('tabPress', (e) => {
  // Prevent default action
  e.preventDefault();
});

```

```javascript

function Profile({ navigation }) {
  React.useEffect(() => {
    const unsubscribe = navigation.addListener('focus', () => {
      // do something
    });

    return unsubscribe;
  }, [navigation]);

  return <ProfileContent />;
}
```