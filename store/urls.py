from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	
	path('aboutus', views.aboutus, name="aboutus"),
	path('contactus', views.contactus, name="contactus"),
	
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

# this is for not easily hack url
	# path("viewdetail/<int:myid>",views.viewdetail,name="viewdetail"),
	path("viewdetail/?utm_source=adwords_ppc&utm_campaignid=1450639170&utm_adgroupid=56780053336&utm_device=c&utm_keyword=&utm_matchtype=&utm_network=d&utm_adpostion=none&utm_creative=474381010056&utm_targetid=aud-463029047231&utm_loc_interest_ms=&utm_loc_physical_ms=1011081&gclid=Cj0KCQjw78yFBhCZARIsAOxgSx2pPD4SHkKD2ThsdIIZIgiNgMwxjNpWckp5c_9U1JMFUoTrHU969QQaAoGoEALw_wcB<int:myid>?utm_source=adwords_ppc&utm_campaignid=1450639170&utm_adgroupid=56780053336&utm_device=c&utm_keyword=&utm_matchtype",views.viewdetail,name="viewdetail"),
# ================================

    path('SearchResults/',views.search,name='search'),

    path('login/',views.handlelogin,name='handlelogin'),
    path('signup/',views.handlesignup,name='handlesignup'),
    
	path('logout/',views.handlelogout,name='handlelogout')
]