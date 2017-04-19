data=csvread('ttest.csv');
% trnData=[data(1:500,3:5),data(1:500,1)];
% chkData=[data(501:end,3:5),data(501:end,1)];
% data2=[data(:,3:5),data(:,2)];
% fismat = genfis1(trnData);
% % [fismat1,error1,ss,fismat2,error2] = ...
% % 	  anfis(trnData,fismat,[],[0 0 0 0],chkData);
% input=data(:,3:5);
% output=data(:,1:2);
data1=[data(:,1:2), data(:,3)];
anfis1 = anfis(data1, 7, 150, [0,0,0,0]);
data2=[data(:,1:2), data(:,4)];
anfis2 = anfis(data2, 6, 150, [0,0,0,0]);
% data3=[data(:,1:2), data(:,5)];
% anfis3 = anfis(data3, 5, 150, [0,0,0,0]);

x=min(data(:,1)):1:max(data(:,1));
y=min(data(:,2)):1:max(data(:,2));
[X,Y]=meshgrid(x,y);
XY=[X(:) Y(:)];
theta1p=evalfis(XY,anfis1);
theta2p=evalfis(XY,anfis2);
%theta3p=evalfis(XY,anfis3);

count1=1;
for i=1:length(XY)
    inp1(XY(i,1),XY(i,2))=theta1p(count1);
    inp2(XY(i,1),XY(i,2))=theta2p(count1);
    count1=count1+1;
end