close all; clear; clc;
set(0,'DefaultFigureWindowStyle','docked');

% Displacement - Force data from Ex_10.1
data1 = importdata( 'coh_ele.rpt');
% Plot data from Ex_10.1
figure(1); axes('LineWidth',2,'FontSize',14);
plot(data1(:,1),data1(:,2),'-k','LineWidth',2);
xlabel('Displacement, [m]','FontSize',16);
ylabel('Reaction Force, [N]','FontSize',16);
axis tight
%Generating Legends
h = legend('Ex 10.1');
set(h,'Interpreter','none','FontSize',14);
%Creating EPS plot
saveas(figure(1),'FigEx101.eps','eps');

disp('--- DONE ---');
