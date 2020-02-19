# coding: utf-8
import scrapy
selector = scrapy.Selector(text="""<div class=\"clear\">
	
		<ul class=\"on1 clear\"><li><b><a href=\"http://english.people.com.cn/n3/2020/0214/c90000-9657881.html\" target=\"_blank\">[WHO Director<font color=\"red\">-</font>General<font color=\"red\">:</font> China doesn<font color=\"red\">'</font>t need to ask to be praised]</a></b></li>
	
</div>""", type="html")


article_name = selector.xpath("//div[@class='clear']/ul[@class='on1 clear']/li/b/a//text()").extract()
print "".join(article_name)

