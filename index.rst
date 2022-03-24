YoutubeTags
===========

**YoutubeTags is a python third-party api wrapper to Extract Youtube
Tags without Youtube API**, **Capable to extract Video and Channel
Tags**

|Downloads| |CodeQL| |Supported Versions| |GitHub| |PyPI| |Documentation
Status| |PyPI - Downloads| |Upload to PIP| |PyPI - Format|

.. |Downloads| image:: https://static.pepy.tech/personalized-badge/youtubetags?period=total&units=abbreviation&left_color=grey&right_color=yellow&left_text=Downloads
   :target: https://pepy.tech/project/youtubetags
.. |CodeQL| image:: https://github.com/nuhmanpk/YoutubeTags/actions/workflows/codeql-analysis.yml/badge.svg
   :target: https://github.com/nuhmanpk/YoutubeTags/actions/workflows/codeql-analysis.yml
.. |Supported Versions| image:: https://img.shields.io/pypi/pyversions/Youtubetags.svg
   :target: https://pypi.org/project/YoutubeTags
.. |GitHub| image:: https://img.shields.io/github/license/nuhmanpk/YoutubeTags
.. |PyPI| image:: https://img.shields.io/pypi/v/youtubetags
.. |Documentation Status| image:: https://readthedocs.org/projects/youtubetags/badge/?version=latest
   :target: https://youtubetags.readthedocs.io/en/latest/?badge=latest
.. |PyPI - Downloads| image:: https://img.shields.io/pypi/dm/YoutubeTags
.. |Upload to PIP| image:: https://github.com/nuhmanpk/YoutubeTags/actions/workflows/Pypi-uploads.yml/badge.svg?branch=main&event=workflow_dispatch
   :target: https://github.com/nuhmanpk/YoutubeTags/actions/workflows/Pypi-uploads.yml
.. |PyPI - Format| image:: https://img.shields.io/pypi/format/YoutubeTags


Installation
============

.. code:: python

   pip install YoutubeTags

Video Tags
==========

How to Use It
-------------

.. code:: python

   import YoutubeTags
   from YoutubeTags import videotags
   link = "Add Your Youtube Link Here" # Use https / http Links
   variable_name = videotags(link)
   print(variable_name)

..

   **NOTE:** ONLY SUPPORTS HTTP(S) , use HTTP(S) links to get the
   results

Example 1
---------

.. code:: python

   import YoutubeTags
   from YoutubeTags import videotags
   findtags = videotags("https://www.youtube.com/watch?v=RTbrXiIzUt4") # Mkbhd's Video
   print(findtags)

Output of Example 1
~~~~~~~~~~~~~~~~~~~

::

   Right To Repair, right to repair, MKBHD, right to repair movement, Apple, Apple vs, 
   repairing iPhone, iPhone 12, Tesla right to repair, Apple right to repair

Example 2
---------

.. code:: python

   import YoutubeTags
   from YoutubeTags import videotags
   tags = videotags("https://www.youtube.com/watch?v=Kbe3FKeCd1A") # Karikku star Episode
   print(tags)

Output of Example 2
~~~~~~~~~~~~~~~~~~~

::

   karikku, malayalam, funny, comedy, webseries, lolan,
   george, karikk, karikke, film, trending, sketch, vine, flowerstv

Example 3
---------

.. code:: python

   import YoutubeTags
   from YoutubeTags import videotags
   gettag = videotags("https://www.youtube.com/watch?v=nvjILgpf6tc") # Video From Technical Guruji
   print(gettag)

Output of Example 3
~~~~~~~~~~~~~~~~~~~

::

   iPhone 14, iPhone 14 Unboxing, iPhone 14 exclusive 1st look, iPhone 14 first look,
   iPhone 14 no notch, iPhone 14 punch hole camera, iPhone 14 titanium sides, iPhone 14 look, 
   iPhone 14 leaks, iPhone 14 design, iPhone 14 india, iPhone 14 launch date, iPhone 14 no camera bump,
   iPhone 14 features, iPhone 14 price, iPhone 14 vs iPhone 13, iPhone 14 launch event, iPhone 14 india 1st look, 
   iPhone 14 first look in hindi, Technical Guruji, Technicalguruji, Gaurav Chaudhary, 13

Example 4 (If Video Has no tags)
--------------------------------

.. code:: python

   import YoutubeTags
   from YoutubeTags import videotags
   tag = videotags("https://www.youtube.com/watch?v=Mlk888FiI8A") # Google Keynote video 2021 
   if tag=="":
      print ("No Tags Found")
   else:
      print(tag)

Output of Example 4
~~~~~~~~~~~~~~~~~~~

::

   No Tags Found

Channel Tags
============

How to Use It
-------------

.. code:: python

   import YoutubeTags
   from YoutubeTags import channeltags
   link = "Add Your Channel Link Here" # Use https / http Links
   variable_name = channeltags(link)
   print(variable_name)

..

   **NOTE:** ONLY SUPPORTS HTTP(S) , use HTTP(S) links to get the
   results

Example 1
---------

.. code:: python

   import YoutubeTags
   from YoutubeTags import channeltags
   findtags = channeltags("https://youtube.com/c/mkbhd") # Mkbhd's channel Link
   print(findtags)

Output of Example 1
~~~~~~~~~~~~~~~~~~~

::

    MKBHD, MarquesBrownlee, Marques, Brownlee 

Example 2
---------

.. code:: python

   import YoutubeTags
   from YoutubeTags import channeltags
   tags = channeltags("https://youtube.com/c/Karikku_Fresh") # Karikku channel Link
   print(tags)

Output of Example 2
~~~~~~~~~~~~~~~~~~~

::

    karikku, media, digital, malayalam

Example 3
---------

.. code:: python

   import YoutubeTags
   from YoutubeTags import channeltags
   gettag = channeltags("https://youtube.com/c/TechnicalGuruji") # Technical Guruji channel Link
   print(gettag)

Output of Example 3
~~~~~~~~~~~~~~~~~~~

::

    Hindi Technology, Technology in Hindi, Hindi Tech Guru, Technical Guruji, Hindi Tech Tips, Tech Reviews, Mobile Tips and Tricks, Technology Explained,
    Hindi Tech, Hindi Tech Reviews, Tech Hindi, hindi, Technology, Mobile, tech, Reviews, TechnicalGuruji, Gaurav Chaudhary, Smartphones, Mobile Phones,
    Tech, latest Tech,Cool Technology, Tech News, Latest Tech News 

Example 4
---------

.. code:: python

   import YoutubeTags
   from YoutubeTags import channeltags
   tag = channeltags("https://youtube.com/user/PewDiePie") # PewDiePie channel Link
   print(tag)

Output of Example 4
~~~~~~~~~~~~~~~~~~~

::

     pewdiepie, pewds, gaming, felix arvid ulf, felix, kjellberg 

License
=======

© 2021 Nuhman Pk , LICENSED under `MIT License`_\ 

Github
------

Follow me on `Github`_ and if you find this `library`_ useful don't
forget to add Your star

Sponsor this project
--------------------

`ko-fi`_\  `paypal`_\  `Buy me a Coffee`_

.. _MIT License: https://github.com/nuhmanpk/YoutubeTags/blob/main/LICENSE
.. _Github: https://www.github.com/nuhmanpk
.. _library: https://github.com/nuhmanpk/YoutubeTags
.. _ko-fi: https://ko-fi.com/nuhmanpk
.. _paypal: https://www.paypal.me/nuhmanpk
.. _Buy me a Coffee: https://www.buymeacoffee.com/nuhmanpk
