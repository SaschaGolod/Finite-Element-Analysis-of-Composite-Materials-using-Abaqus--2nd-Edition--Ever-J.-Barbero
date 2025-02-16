close all; clear; clc;
set(0,'DefaultFigureWindowStyle','docked');

% Displacement - Force data from Ex_10.3
data3 = importdata( 'vcct.rpt');
% Plot data from Ex_10.3
figure(1); axes('LineWidth',2,'FontSize',14);
plot(data3(:,1),data3(:,2),'-k','LineWidth',2);
xlabel('Displacement, [m]','FontSize',16);
ylabel('Reaction Force, [N]','FontSize',16);
axis tight
%Generating Legends
h = legend('Ex 10.3');
set(h,'Interpreter','none','FontSize',14);
%Creating EPS plot
saveas(figure(1),'FigEx103.eps','eps');

%%
% Displacement - Force data from Ex_10.1
data1 = importdata( 'coh_ele.rpt');
data2 = importdata( 'coh_surf.rpt');
% Plot data from Ex_10.1
figure(2); axes('LineWidth',2,'FontSize',14);
plot(data1(:,1),data1(:,2),':k','LineWidth',2);
figure(2); hold on;
plot(data2(:,1),data2(:,2),'--k','LineWidth',2);
plot(data3(:,1),data3(:,2),'-k','LineWidth',2);
xlabel('Displacement, [m]','FontSize',16);
ylabel('Reaction Force, [N]','FontSize',16);
axis tight
%Generating Legends
h = legend('cohesive elements','cohesive surfaces','VCCT');
set(h,'Interpreter','none','FontSize',14);
%Creating EPS plot
saveas(figure(2),'FigEx101Ex102Ex103.eps','eps');

disp('--- DONE ---');
