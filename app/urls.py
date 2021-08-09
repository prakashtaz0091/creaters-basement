from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name = 'home'),
    # path('adminPage',views.adminPage,name='adminPage'),
    path('registerPage/',views.registerPage,name='registerPage'),
    path('loginPage/',views.loginPage,name='loginPage'),
    path('logoutUser/',views.logoutUser,name='logoutUser'),

    # path('aboutus/',views.about, name='about'),
    path('tracks/',views.tracks, name='tracks'),
    # path('projects/',views.projects, name='projects'),
    # path('recording/',views.recording, name='recording'),
    path('contact-us/',views.contactUs, name='contactUs'),
    path('view-messages/',views.viewMessages, name='viewMessages'),
    path('reply-message/',views.replyMessage, name='replyMessage'),
    path('delete-message/<int:pk>/',views.deleteMessage, name='deleteMessage'),


    path('newmusic/',views.newMusic, name='newMusic'),

    path('upload/',views.uploadContent, name='uploadContent'),
    path('upload-user/',views.uploadContentUser, name='uploadContentUser'),
    path('get-final-product/',views.getFinalProduct, name='getFinalProduct'),
    path('delete-userfile/<int:pk>/',views.deleteUserFile, name='deleteUserFile'),


    path('user-uploaded/contents/',views.viewUserUploadedContents, name='viewUserUploadedContents'),
    path('uploadfinal/product/<int:pk>/',views.uploadFinalProduct, name='uploadFinalProduct'),


    path('completed-projects/',views.viewCompletedProjects, name='viewCompletedProjects'),


    path('inform-customer/<int:pk>',views.informCustomer, name='informCustomer'),
    
    
    path('upload-original/<int:pk>',views.uploadOriginal, name='uploadOriginal'),
    path('view-original/',views.viewOriginal, name='viewOriginal'),
    path('delete/<int:pk>/',views.delete, name='delete'),
    path('memories/',views.memories, name='memories'),
    path('remove-memories/<int:pk>/',views.removeMemories, name='removeMemories'),

    path('get-our-music/',views.getOurMusic,name='getOurMusic'),

    # path('buy/<int:pk>/',views.buy,name='buy'), #main buy
    path('buy-from-store/<int:pk>/',views.buyFromStore,name='buyFromStore'), #if user buys from store
    path('buy-from-projects/<int:pk>/',views.buyFromProjects,name='buyFromProjects'), #if user buys the edited version of their raw project


    path('cart/',views.cart,name='cart'),
    path('set-price/<int:pk>/',views.setPrice,name='setPrice'),

    path('set-price-completed/<int:pk>/',views.setPriceCompleted,name='setPriceCompleted'),

    path('esewa-verification/',views.esewaVerify, name='esewaVerify'),



    path('addYoutubeLink/',views.addYoutubeLink,name='addYoutubeLink'),
    path('removeYoutubeLink/<int:pk>/',views.removeYtLink,name='removeYtLink'),


    path('edit/<str:label>/',views.edit,name='edit'),


    path('request-demo/<int:pk>/',views.requestDemo,name='requestDemo'),
    path('view-demo-requests/',views.viewDemoRequest,name='viewDemoRequest'),


    path('video-gallery/',views.videoGallery,name='videoGallery'),



] 

 