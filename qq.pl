#!/usr/bin/env perl
use Mojo::Webqq;
my ($qq,$host,$port,$post_api);

$qq = 859044664;    #修改为你自己的实际QQ号码
$host = "0.0.0.0"; #发送消息接口监听地址，修改为自己希望监听的地址
$port = 5000;      #发送消息接口监听端口，修改为自己希望监听的端口
$post_api = 'http://127.0.0.1:8892/gateway.test';  #接收到的消息上报接口，如果不需要接收消息上报，可以删除此行

my $client = Mojo::Webqq->new(qq=>$qq);

$client->login();
$client->load("ShowMsg");
$client->load("Openqq",data=>{listen=>[{host=>$host,port=>$port}], post_api=>$post_api});
$client->run();
