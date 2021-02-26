---
layout: post
title: In defence of web scraping
date: 2019-11-01 10:18:00
tags: philosophy
---

SOURCE:

- [Open internet](https://hackernoon.com/web-scraping-and-the-fight-for-the-open-internet-ly1o2t8i)
- [Big data and web scraping](https://hackernoon.com/the-evolution-of-big-data-and-web-scraping-mk1y3ucv)
- Season 3 of westworld
- [Robots_exclusion_standard](https://en.wikipedia.org/wiki/Robots_exclusion_standard)
- [Search_engine_scraping](https://en.wikipedia.org/wiki/Search_engine_scraping)
- [TheProject](http://info.cern.ch/hypertext/WWW/TheProject.html)

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/service.png)</span>

When I say to people that I'm doing "web scraping" for my personal project, they either don't know what I'm talking about or look at me with eyes of fear. The term "web scraping" has a negative connotation today. It's often seen as unethical or/and illegal.

# Why illegal?

Some companies could even sue you (there have been dozens of legal cases on web scraping over the decades) or do some lobbying to make it illegal. It might not work but it gives a force of dissuasion: people might experience the guilt of doing something illegal.

# Why unethical?

Of course, if you read the news, you might be thinking of Cambridge Analytica or other organizations that scraps social media user data and manipulate by sending advertisements, fake news...

We realize today that you can do web scraping to sell data to states, industries, advertisement companies or to rig an election. All this is, of course, harmful because the end goal is control and manipulation (pushing people to buy, to vote for the person who pays for you...). If the end goal is only money, power and control, we will end up with ads, surveillance everywhere. The web will become senseless and data will become a simple tool for controlling humans. Season 3 of westworld or episode 1 season 3 of black mirror gives us a good illustration of what we need to avoid.

<p style="text-align:center"><iframe width="100%" height="315" src="https://www.youtube.com/embed/YrpK90bHO2U" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></p>

If you want a centralized computer that monitors everything, and data with one owner, you need to be like Facebook and ask users to hand over their data by means of an authentication system. If the technological architecture is designed this way, the data will belong to the company and no one else. If you decide to put all the data collected by users behind an authentication system, you decide not to share data, but to keep it for yourself.

<p style="text-align:center"><video width="100%" height="500" controls> <source src="{{site.baseurl}}/assets/BLACK.mp4" type="video/mp4"> </video></p>

All this is pretty bad, I agree. But it doesn't necessarily mean that we need to condemn web scraping. I would like to rehabilitate this practice if it's OK and see if we can change direction.

But to do this, we need to go back first to the basics and see what a cool thing the web actually is.

# What is the web?

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/document.png)</span>

<p style="text-align:center"><iframe width="100%" height="315" src="https://www.youtube.com/embed/_mNOXDbXr9c" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></p>

The web is basically linked documents (you click on a link and it brings you to another document from a specific computer). These linked documents can be shown by asking a specific computer to download it into your browser with an http/https protocol.

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/http.png)</span>

We call these computers 'servers' because they are configured in such a way that it can listen to our requests. 'Servers' turn a program in background waiting for some messages to come so that it can answer and deliver the required document or data.

The content of these html documents is digital data. Why digital? Because they are binary (0 1). The browser translates this binary data to data that a human can understand.

This is maybe a basic definition of what we call the web. The enormous value of it today is that all these documents, coming from different computers are linked together (with hyperlinks). Like university papers, or academic books, they often provide sources.

It's extremely important to note that there is no super-computer that monitors all these documents. Nor are there any super computers that monitor all these little computers. The information is spread horizontally in a decentralized way, through different computers.

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/decentralized.png)</span>

When everything seems to be controlled by an institution, a company, a state in the offline world..., no one really controls the online world and some even say that this world has been made (not really by the us army, but by everyone of us that decides to add document files on the web) to be uncontrollable.

In summary, we can see the web as an enormous library of documents linked to each other with no owner. If data had owners and strict copyright, we would not be able to build a search engine. The web would become a very messy library with no way of finding the documents that users really need.

<span style="display:block;text-align:center">![Octocat]({{site.baseurl}}/assets/img/library.jpeg)</span>

# What is web scraping now?

<em>"The largest public known incident of a search engine being scraped happened in 2011 when Microsoft was caught scraping unknown keywords from Google for their own, rather new Bing service. But even this incident did not result in a court case."</em>

<em>"One possible reason might be that search engines like Google are getting almost all their data by scraping millions of public reachable websites, also without reading and accepting those terms. A legal case won by Google against Microsoft would possibly put their whole business as risk."</em>

[Wikipedia: Search engine scraping](https://en.wikipedia.org/wiki/Search_engine_scraping)

Web scraping is an automated way to collect data from the web. If an API is not available, often, what needs to be done is taking a website’s HTML file, detecting the data and saving it, often into a database. So once the data is public, on the web, someone can store, monitor and/or use it.

If people don't want to access good content, it's not the fault of the web. And this problem is not technical. It's ethical. If we build a new architecture of the web but behaviors do not change, we will have new types of Facebook coming along. We don't need to build a more decentralized web with other technologies, we already need to be aware of the existing potentials of the web.

<p style="text-align:center"><video width="100%" height="500" controls> <source src="{{site.baseurl}}/assets/google2.mp4" type="video/mp4"> </video></p>

The dream of one of the co-founders of google was to download the html documents of all the web, save it on his computer and do a big network of nodes based on the links he could find on each web (html) documents. He would need to first make a rule that recognizes links within webpages, transforms the link into a node and see where it is positioned in this big network.

We can easily see here that Google is today’s most advanced web scraping company in existence. And, if we really want to access it, Google’s web scraping gives us the most amazing access to culture (with a big C) that there is.

With these web scraping techniques, Google has given us a web that is easy to navigate.
A web that is decipherable.

# No Web Scraping, no search engine

<p style="text-align:center"><video width="100%" controls> <source src="{{site.baseurl}}/assets/google4.mp4" type="video/mp4"> </video></p>

Without search engines like Google, the web would be nearly impossible to use. We would not be able to find out what we could do with it or the easy access would only be information from people of big influence like politicians, celebrities of the star system, or powerful advertisement companies.

<p style="text-align:center"><video width="100%" height="500" controls> <source src="{{site.baseurl}}/assets/google.mp4" type="video/mp4"> </video></p>

# So now where can we go?

I think we didn't grab very well the potential of web scraping today and it's normal because it's not easy. Of course the first thing that comes into our mind is to use web scraping to find cheap prices for plane tickets, restaurants, products... Which is great. But we maybe can find an even better use for it.

Today, we realize that the web is the perfect thing for big data. No web, no big data, no big data, no machine learning. We have powerful enough machines now to process a lot of the data and make sense of it.

We now have machine-learning techniques that scrape the web and can process and classify data in order to:

- detect a serious illness fast, before it's too late
- detect a forest fire before it’s too late
- detect dangerous substances in a food product
- detect dangers to plant, animal or insect life (such as the varroa mite to bee populations)
- detect an outbreak of a new disease before it’s too late
- detect dangerous substances of product we're eating
- automatized customer services that use advanced chatbots to problem-solve help you mend stuff (by sending photos to them) and find what you need to buy for you
- these chatbot could help you mend stuff (by sending photos to them) and find what you need to buy for you
- machine learning can give us very precise statistics in economy, urbanism, criminality …
...

Other suggestions?

Web scraping is useful here because we need classified data to detect something. For example, we can scrap images of skin cancer everywhere on the web and classify to automatically detect it on a random photo. We can scrap images of forest fire so that cameras can recognize a danger automatically.

In summary, Web scraping can give us better access to culture, science, and with better access to culture, science... humans can maybe act in the world with greater attention to important things and/or awareness.